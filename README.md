# Xbox SFTP to SSH Tool

A testing and learning project im making for a graphical Xbox One SFTP client with file browsing, memory tools, payload execution, and Hydra integration.  
This project is still a **work-in-progress**, but now includes several functional modules.

---

## ✅ Features (Working & Planned)

- ✅ Xbox One file browser with folder navigation  
- ✅ Includes *auto drive scan* and *back button support*
- ✅ SFTP connect/disconnect UI
- ✅ File upload/download
- ✅ Raw Hydra command interface
- ✅ Version check (Hydra build & protocol check)
- ✅ Integrated Hydra Control Panel

**Experimental / In Progress**
- 🚧 Memory read/write (peek/poke)
- 🚧 Toast notification support *(early test — documentation coming soon!)*
- 🚧 Payload injection/execution
- 🚧 App/game listing

---

## 🧪 What’s Next?

We’re working toward a full setup experience for:
- **Collateral Damage** (Xbox One kernel exploit)
- **Durango SSH server** (SSH access on Xbox)
- One-click setup to replicate dev-like environments on retail systems

The goal is to make everything easier to use, like a plug-and-play Windows setup.  
This also includes a **full tutorial and documentation** built around all known public information to help others jump in faster.

> A lot of this is developer-focused for now, and has been behind-the-scenes for a while.  
> I’m just the middle-man trying to bring it together and **get more people involved**. This is a team effort by the community 💚

---

## 🔗 Links & Resources

- 💥 Collateral Damage:  
  https://github.com/exploits-forsale/collateral-damage

- 🧠 LittleHydra (used in this tool):  
  https://github.com/xboxoneresearch/LittleHydra

- 🌐 Durango Portal (Xbox SSH server):  
  https://github.com/xboxoneresearch/durango-portal

- 📢 Background info and notes:  
  https://www.reddit.com/r/XboxRetailHomebrew/comments/1lf8ry6/findings_xbox_one_uwp_exploit_update/

- 📚 Xbox One Research Docs:  
  https://xboxoneresearch.github.io/wiki/

  Video TUT:
  https://www.youtube.com/watch?v=jp5I9q-TM6o

---

## 🛠 Requirements

- Python 3.9+
- Git (to clone/update)
- Xbox One running Durango SFTP

🙏 Special Thanks
Tuxuser – for their extensive work, dedication, and public contributions to the Xbox research and homebrew community.
Much of this tool’s direction and purpose is built on foundations made possible by their insight, tools, and support.

https://github.com/tuxuser

### Setup:

```bash
git clone https://github.com/Mullin5478/xbox-sftp-tool.git
cd xbox-sftp-tool
pip install -r requirements.txt
python main.py
