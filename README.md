# Xbox SFTP Tool

A testing and learning project for a graphical Xbox SFTP client with file browsing, payload uploading, and more. **This project is a work-in-progress and not fully functional yet.**

## ⚠️ Disclaimer

**This tool is currently in early development / prototype phase.**
- Some features may not work or are just stubs for now (UI buttons, etc).
- Use at your own risk! Bug reports, feedback.

## Features (Planned & Partial)

- [x] Basic Xbox file browser
- [x] File upload/download
- [x] Connect/disconnect to SFTP server
- [ ] Payload injection/execution (incomplete)
- [ ] Memory dump tools (testing)
- [ ] Toast notifications (testing)
- [ ] App/game listing (in progress)
- [ ] Hydra panel integration (if available)




pip install -r requirements.txt
run:

python main.py


This tool requires your Xbox One to be running an SFTP server.  
I recommend [xboxoneresearch/durango-portal](https://github.com/xboxoneresearch/durango-portal):

1. Follow the instructions at [https://github.com/xboxoneresearch/durango-portal](https://github.com/xboxoneresearch/durango-portal) to install and start the SFTP server on your Xbox.
2. Take note of the Xbox’s IP address and the login credentials set for SFTP.
3. Use those credentials in this app to connect and browse/upload/download files.
