"""
Main contract implementation for the Digital Marketplace.
"""
from typing import Dict, Optional, List, Tuple
import base64

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.error import AlgodHTTPError

from .config import (
    TOTAL_SUPPLY,
    DECIMALS,
    FIXED_FEE_USDT,
    STAKING_THRESHOLD_USDT,
    STAKING_REWARD_PERCENTAGE
)
from .utils import (
    algo_to_usdt,
    usdt_to_algo,
    get_current_timestamp,
    format_amount
)

class DigitalMarketplace:
    def __init__(self, algod_client: algod.AlgodClient, creator_address: str, 
                 creator_private_key: str, github_handle: str):
        """
        Initialize the Digital Marketplace contract.
        
        Args:
            algod_client: An initialized Algorand client
            creator_address: The Algorand address of the contract creator
            creator_private_key: The private key of the contract creator
            github_handle: The GitHub username of the deployer
        """
        self.algod_client = algod_client
        self.creator_address = creator_address
        self.creator_private_key = creator_private_key
        self.github_handle = github_handle
        self.asset_id = None
        self.token_holders: Dict[str, int] = {}
        self.staking_rewards: Dict[str, int] = {}
        self.last_staking_calculation = get_current_timestamp()

    def create_token(self) -> int:
        """
        Create the digital marketplace token with the specified parameters.
        
        Returns:
            int: The asset ID of the created token
        """
        if self.asset_id is not None:
            raise ValueError("Token has already been created")
        
        # Get suggested parameters from the network
        params = self.algod_client.suggested_params()
        
        # Define the asset parameters
        unit_name = "DMARKET"
        asset_name = "Digital Marketplace Token"
        url = "https://digitalmarketplace.example.com"
        metadata_hash = b""  # Could add a hash of metadata here if needed
        
        # Create the asset creation transaction
        txn = transaction.AssetConfigTxn(
            sender=self.creator_address,
            sp=params,
            total=TOTAL_SUPPLY * (10 ** DECIMALS),  # Adjusted for decimals
            default_frozen=False,
            unit_name=unit_name,
            asset_name=asset_name,
            manager=self.creator_address,
            reserve=self.creator_address,
            freeze=self.creator_address,
            clawback=self.creator_address,
            url=url,
            metadata_hash=metadata_hash,
            decimals=DECIMALS
        )
        
        # Sign the transaction
        signed_txn = txn.sign(self.creator_private_key)
        
        # Submit the transaction to the network
        try:
            tx_id = self.algod_client.send_transaction(signed_txn)
            print(f"Transaction ID: {tx_id}")
            
            # Wait for confirmation
            confirmed_txn = transaction.wait_for_confirmation(self.algod_client, tx_id, 4)
            asset_id = confirmed_txn["asset-index"]
            print(f"Asset ID created: {asset_id}")
            
            self.asset_id = asset_id
            
            # Initialize the creator's balance with the total supply
            self.token_holders[self.creator_address] = TOTAL_SUPPLY * (10 ** DECIMALS)
            
            return asset_id
        
        except AlgodHTTPError as e:
            print(f"Failed to create asset: {e}")
            raise

    def deposit(self, sender_address: str, sender_private_key: str, algo_amount: int) -> Tuple[str, int]:
        """
        Deposit ALGO and receive equivalent tokens minus fees.
        Also stores the GitHub handle in a box.
        """
        if self.asset_id is None:
            raise ValueError("Token has not been created yet")
        
        # Create box for GitHub handle if it doesn't exist
        box_name = "github"
        box_value = self.github_handle.encode()
        
        # Get suggested parameters
        params = self.algod_client.suggested_params()
        
        # Create box storage transaction
        box_txn = transaction.ApplicationCallTxn(
            sender=sender_address,
            sp=params,
            index=self.asset_id,
            on_complete=transaction.OnComplete.NoOp,
            app_args=["set_github"],
            boxes=[(self.asset_id, box_name.encode())]
        )
        
        # Convert ALGO to USDT equivalent for token calculation
        usdt_equivalent = algo_to_usdt(algo_amount)
        
        # Calculate fee in USDT (fixed fee per transaction)
        fee_usdt = FIXED_FEE_USDT
        
        # Convert fee to ALGO
        fee_algo = usdt_to_algo(fee_usdt)
        
        # Calculate net USDT amount after fee
        net_usdt = usdt_equivalent - fee_usdt
        
        # Calculate tokens to be received (1:1 with USDT for simplicity)
        tokens_to_receive = int(net_usdt * (10 ** DECIMALS))
        
        if tokens_to_receive <= 0:
            raise ValueError("Deposit amount too small to cover fees")
        
        # Check if we have enough tokens left
        available_tokens = self.token_holders.get(self.creator_address, 0)
        if available_tokens < tokens_to_receive:
            raise ValueError("Not enough tokens available for this deposit")
        
        # Create the payment transaction for the ALGO
        payment_txn = transaction.PaymentTxn(
            sender=sender_address,
            sp=params,
            receiver=self.creator_address,
            amt=algo_amount
        )
        
        # Create the asset transfer transaction for the tokens
        asset_txn = transaction.AssetTransferTxn(
            sender=self.creator_address,
            sp=params,
            receiver=sender_address,
            amt=tokens_to_receive,
            index=self.asset_id
        )
        
        # Group all transactions
        transaction.assign_group_id([box_txn, payment_txn, asset_txn])
        
        # Sign all transactions
        signed_box_txn = box_txn.sign(sender_private_key)
        signed_payment_txn = payment_txn.sign(sender_private_key)
        signed_asset_txn = asset_txn.sign(self.creator_private_key)
        
        # Submit the transactions
        try:
            tx_id = self.algod_client.send_transactions([signed_box_txn, signed_payment_txn, signed_asset_txn])
            print(f"Transaction ID: {tx_id}")
            
            # Wait for confirmation
            transaction.wait_for_confirmation(self.algod_client, tx_id, 4)
            
            # Update token balances
            self.token_holders[self.creator_address] = available_tokens - tokens_to_receive
            current_balance = self.token_holders.get(sender_address, 0)
            self.token_holders[sender_address] = current_balance + tokens_to_receive
            
            return tx_id, tokens_to_receive
            
        except AlgodHTTPError as e:
            print(f"Failed to process deposit: {e}")
            raise

    def withdraw(self, sender_address: str, sender_private_key: str, token_amount: int) -> Tuple[str, int]:
        """
        Withdraw tokens and receive equivalent ALGO minus fees.
        
        Args:
            sender_address: The Algorand address of the sender
            sender_private_key: The private key of the sender
            token_amount: The amount of tokens to withdraw
            
        Returns:
            Tuple[str, int]: Transaction ID and ALGO received
        """
        if self.asset_id is None:
            raise ValueError("Token has not been created yet")
        
        # Check if sender has enough tokens
        sender_balance = self.token_holders.get(sender_address, 0)
        if sender_balance < token_amount:
            raise ValueError("Not enough tokens to withdraw")
        
        # Calculate USDT equivalent of tokens (1:1 for simplicity)
        usdt_equivalent = token_amount / (10 ** DECIMALS)
        
        # Calculate fee in USDT (fixed fee per transaction)
        fee_usdt = FIXED_FEE_USDT
        
        # Calculate net USDT amount after fee
        net_usdt = usdt_equivalent - fee_usdt
        
        if net_usdt <= 0:
            raise ValueError("Withdrawal amount too small to cover fees")
        
        # Convert USDT to ALGO
        algo_to_send = usdt_to_algo(net_usdt)
        
        # Get suggested parameters from the network
        params = self.algod_client.suggested_params()
        
        # Create the asset transfer transaction for the tokens
        asset_txn = transaction.AssetTransferTxn(
            sender=sender_address,
            sp=params,
            receiver=self.creator_address,
            amt=token_amount,
            index=self.asset_id
        )
        
        # Create the payment transaction for the ALGO
        payment_txn = transaction.PaymentTxn(
            sender=self.creator_address,
            sp=params,
            receiver=sender_address,
            amt=algo_to_send
        )
        
        # Group the transactions
        transaction.assign_group_id([asset_txn, payment_txn])
        
        # Sign the transactions
        signed_asset_txn = asset_txn.sign(sender_private_key)
        signed_payment_txn = payment_txn.sign(self.creator_private_key)
        
        # Submit the transactions to the network
        try:
            tx_id = self.algod_client.send_transactions([signed_asset_txn, signed_payment_txn])
            print(f"Transaction ID: {tx_id}")
            
            # Wait for confirmation
            transaction.wait_for_confirmation(self.algod_client, tx_id, 4)
            
            # Update token balances
            self.token_holders[sender_address] = sender_balance - token_amount
            creator_balance = self.token_holders.get(self.creator_address, 0)
            self.token_holders[self.creator_address] = creator_balance + token_amount
            
            return tx_id, algo_to_send
        
        except AlgodHTTPError as e:
            print(f"Failed to process withdrawal: {e}")
            raise
    
    def calculate_staking_rewards(self) -> None:
        """
        Calculate staking rewards for eligible token holders.
        
        Holders with tokens worth 10K+ USDT are eligible for 5% rewards in ALGO.
        """
        current_time = get_current_timestamp()
        
        # Calculate time elapsed since last calculation in seconds
        time_elapsed = current_time - self.last_staking_calculation
        
        # Only calculate rewards once per day (86400 seconds)
        if time_elapsed < 86400:
            return
        
        # Update the timestamp for the next calculation
        self.last_staking_calculation = current_time
        
        # Calculate rewards for each eligible holder
        for address, token_balance in self.token_holders.items():
            # Convert token balance to USDT
            usdt_value = token_balance / (10 ** DECIMALS)
            
            # Check if holder is eligible for staking rewards
            if usdt_value >= STAKING_THRESHOLD_USDT:
                # Calculate yearly reward in USDT
                yearly_reward_usdt = usdt_value * (STAKING_REWARD_PERCENTAGE / 100)
                
                # Calculate daily reward in USDT
                daily_reward_usdt = yearly_reward_usdt / 365
                
                # Convert USDT reward to ALGO
                daily_reward_algo = usdt_to_algo(daily_reward_usdt)
                
                # Add to holder's staking rewards
                current_rewards = self.staking_rewards.get(address, 0)
                self.staking_rewards[address] = current_rewards + daily_reward_algo
    
    def claim_staking_rewards(self, holder_address: str) -> Tuple[str, int]:
        """
        Allow a holder to claim their accumulated staking rewards.
        
        Args:
            holder_address: The Algorand address of the token holder
            
        Returns:
            Tuple[str, int]: Transaction ID and ALGO claimed
        """
        # Check if holder has any rewards
        reward_balance = self.staking_rewards.get(holder_address, 0)
        if reward_balance <= 0:
            raise ValueError("No staking rewards available to claim")
        
        # Get suggested parameters from the network
        params = self.algod_client.suggested_params()
        
        # Create the payment transaction for the ALGO rewards
        payment_txn = transaction.PaymentTxn(
            sender=self.creator_address,
            sp=params,
            receiver=holder_address,
            amt=reward_balance
        )
        
        # Sign the transaction
        signed_payment_txn = payment_txn.sign(self.creator_private_key)
        
        # Submit the transaction to the network
        try:
            tx_id = self.algod_client.send_transaction(signed_payment_txn)
            print(f"Transaction ID: {tx_id}")
            
            # Wait for confirmation
            transaction.wait_for_confirmation(self.algod_client, tx_id, 4)
            
            # Reset the holder's staking rewards
            claimed_amount = reward_balance
            self.staking_rewards[holder_address] = 0
            
            return tx_id, claimed_amount
        
        except AlgodHTTPError as e:
            print(f"Failed to claim staking rewards: {e}")
            raise
    
    def get_token_balance(self, address: str) -> int:
        """
        Get the token balance for a specific address.
        
        Args:
            address: The Algorand address to check
            
        Returns:
            int: The token balance
        """
        return self.token_holders.get(address, 0)
    
    def get_staking_rewards(self, address: str) -> int:
        """
        Get the pending staking rewards for a specific address.
        
        Args:
            address: The Algorand address to check
            
        Returns:
            int: The pending staking rewards in microALGO
        """
        return self.staking_rewards.get(address, 0)
    
    def get_token_info(self) -> dict:
        """
        Get information about the token.
        
        Returns:
            dict: Token information
        """
        if self.asset_id is None:
            raise ValueError("Token has not been created yet")
        
        try:
            asset_info = self.algod_client.asset_info(self.asset_id)
            return asset_info
        
        except AlgodHTTPError as e:
            print(f"Failed to get token info: {e}")
            raise