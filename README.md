
# Xbox SFTP to SSH Tool

A testing and learning project im making for a graphical Xbox One SFTP client with file browsing, memory tools, payload execution, and Hydra integration.  
This project is still a **work-in-progress**, but now includes several functional modules.

# ✅ Features (Working & Planned)

* ✅ Xbox One file browser with folder navigation
* ✅ Includes *auto drive scan* and *back button support*
* ✅ SFTP connect/disconnect UI
* ✅ File upload/download
* ✅ Raw Hydra command interface
* ✅ Version check (Hydra build & protocol check)
* ✅ Integrated Hydra Control Panel
* ✅ progress bar added
* ✅ dumping games via o drive needs more work (working but runs in main thread need moving to new thread) done but slow took 6+ hr for 43gb file likely due to the network.

**Experimental / In Progress**

* 🚧 Memory read/write (peek/poke)
* 🚧 Toast notification support *(early test — documentation coming soon!)*
* 🚧 Payload injection/execution
* 🚧 App/game listing

# 🧪 What’s Next?

We’re working toward a full setup experience for:

* **Collateral Damage** (Xbox One kernel exploit)
* **Durango SSH server** (SFTP access on Xbox)
* One-click setup to replicate dev-like environments on retail systems

The goal is to make everything easier to use, like a plug-and-play Windows setup.  
This also includes a **full tutorial and documentation** built around all known public information to help others jump in faster.

>A lot of this is developer-focused for now, and has been behind-the-scenes for a while.  
I’m just the middle-man trying to bring it together and **get more people involved**. This is a team effort by the community 💚

# 🔗 Links & Resources
https://github.com/Mullin5478/xbox-sftp-tool
The tool: 

* 💥 Collateral Damage: [https://github.com/exploits-forsale/collateral-damage](https://github.com/exploits-forsale/collateral-damage)
* 🧠 LittleHydra (used in this tool): [https://github.com/xboxoneresearch/LittleHydra](https://github.com/xboxoneresearch/LittleHydra)
* 🌐 Durango Portal (Xbox SFTP server): [https://github.com/xboxoneresearch/durango-portal](https://github.com/xboxoneresearch/durango-portal)
* 📢 Background info and notes: [https://www.reddit.com/r/XboxRetailHomebrew/comments/1lf8ry6/findings\_xbox\_one\_uwp\_exploit\_update/](https://www.reddit.com/r/XboxRetailHomebrew/comments/1lf8ry6/findings_xbox_one_uwp_exploit_update/)
* 📚 Xbox One Research Docs: [https://xboxoneresearch.github.io/wiki/](https://xboxoneresearch.github.io/wiki/)

# 🛠 Requirements

* Python 3.9+
* Git (to clone/update)
* Xbox One running Durango SFTP

![img](n39zbtfqeodf1)

    git clone https://github.com/Mullin5478/xbox-sftp-tool.git
    cd xbox-sftp-tool
    pip install -r requirements.txt
    python main.py
    
    
    🖼️ **Screenshots**
    
    ![img](kr6xa676wicf1)
    
