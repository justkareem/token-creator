import os

import requests
import json
import uuid
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solders.commitment_config import CommitmentLevel
from solders.rpc.requests import SendVersionedTransaction
from solders.rpc.config import RpcSendTransactionConfig
import asyncio
from tweetcapture import TweetCapture

PRIVATE_KEY = "*******"


# Function to capture a tweet screenshot asynchronously
async def capture_tweet(tweet_url):
    tweet_capturer = TweetCapture()
    image_path = await tweet_capturer.screenshot(tweet_url)
    if image_path:
        output_image_path = f"tweet_image_{uuid.uuid4().hex}.png"
        os.rename(image_path, output_image_path)
        print(f"Screenshot saved at: {output_image_path}")
        return output_image_path
    else:
        print("Failed to capture the tweet.")
        return None


# Function: Launch coin on Pump-Fun and buy it
def send_local_create_tx(coin_details, tweet_details):
    try:
        # Load the signer's keypair
        signer_keypair = Keypair.from_base58_string(PRIVATE_KEY)

        # Generate a random keypair for token mint
        mint_keypair = Keypair()

        # Determine image path to use
        image_path = None
        if coin_details['image']:
            try:
                # Download the first image in media_urls
                image_response = requests.get(coin_details['image'])
                image_response.raise_for_status()
                image_path = f"temp_image_{uuid.uuid4().hex}.jpg"
                with open(image_path, "wb") as img_file:
                    img_file.write(image_response.content)
            except requests.RequestException as e:
                print(f"Error downloading image {coin_details['image']}: {e}")
        else:
            # Download a screenshot of the tweet
            tweet_url = f"https://x.com/{tweet_details['author_screen_name']}/status/{tweet_details['id_str']}"
            image_path = asyncio.run(capture_tweet(tweet_url))

        if not image_path:
            print("Error: No image available for token creation.")
            return

        # Define token metadata form data
        form_data = {
            'name': coin_details['name'],
            'symbol': coin_details['ticker'],
            'description': coin_details['description'],
            'twitter': f"https://x.com/{tweet_details['author_screen_name']}/status/{tweet_details['id_str']}",
            'telegram': f"https://x.com/{tweet_details['author_screen_name']}/status/{tweet_details['id_str']}",
            'website': f"https://x.com/{tweet_details['author_screen_name']}/status/{tweet_details['id_str']}",
            'showName': 'true'
        }

        # Read and upload the image file
        try:
            with open(image_path, 'rb') as f:
                file_content = f.read()

            files = {
                'file': (os.path.basename(image_path), file_content, 'image/jpeg')
            }

            # Create IPFS metadata storage
            metadata_response = requests.post("https://pump.fun/api/ipfs", data=form_data, files=files)
            metadata_response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.RequestException as e:
            print(f"Error during IPFS metadata storage: {e}")
            return
        finally:
            # Delete the image file after uploading
            if os.path.exists(image_path):
                os.remove(image_path)

        metadata_response_json = metadata_response.json()
        if 'metadataUri' not in metadata_response_json:
            print("Error: metadataUri not found in the response")
            return

        # Token metadata
        token_metadata = {
            'name': form_data['name'],
            'symbol': form_data['symbol'],
            'uri': metadata_response_json['metadataUri']
        }

        # Generate the create transaction
        try:
            response = requests.post(
                "https://pumpportal.fun/api/trade-local",
                headers={'Content-Type': 'application/json'},
                data=json.dumps({
                    'publicKey': str(signer_keypair.pubkey()),
                    'action': 'create',
                    'tokenMetadata': token_metadata,
                    'mint': str(mint_keypair.pubkey()),
                    'denominatedInSol': 'true',
                    'amount': coin_details["meme_level"],  # Dev buy of 1 SOL
                    'slippage': 0,
                    'priorityFee': 0.0000,
                    'pool': 'pump'
                })
            )
            response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.RequestException as e:
            print(f"Error creating transaction: {e}")
            return

        tx_bytes = response.content
        try:
            tx_message = VersionedTransaction.from_bytes(tx_bytes).message
            tx = VersionedTransaction(tx_message, [mint_keypair, signer_keypair])
        except Exception as e:
            print(f"Error deserializing transaction: {e}")
            return

        # Send the transaction to the Solana network
        commitment = CommitmentLevel.Confirmed
        config = RpcSendTransactionConfig(preflight_commitment=commitment)
        tx_payload = SendVersionedTransaction(tx, config)

        try:
            rpc_response = requests.post(
                url="https://api.mainnet-beta.solana.com/",
                headers={"Content-Type": "application/json"},
                data=tx_payload.to_json()
            )
            rpc_response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.RequestException as e:
            print(f"Error sending transaction: {e}")
            return

        # Parse and print the transaction signature
        rpc_response_json = rpc_response.json()
        if 'result' in rpc_response_json:
            tx_signature = rpc_response_json['result']
            print(f'Transaction: https://solscan.io/tx/{tx_signature}')
        else:
            print(f"Error: Unexpected response from RPC: {rpc_response_json}")

    except Exception as e:
        print(f"An error occurred: {e}")
