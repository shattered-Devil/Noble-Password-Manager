# Noble Password Manager v0.0.4
## Build Dependencies and Installation Commands

This document explains how to prepare a Windows Python environment for building Noble Password Manager from source.

> **Project:** Noble Password Manager  
> **Version:** 0.0.4 Beta  
> **Platform:** Windows x64

---

## 1. Requirements File

Create or keep this file next to the source code:

`NoblePasswordManager_requirements.txt`

Its contents:

```text
arabic-reshaper==3.0.1
customtkinter==6.0.0
cryptography==49.0.0
Pillow==12.3.0
python-bidi==0.6.11
Nuitka==4.1.3
```

---

## 2. Open CMD in the Project Folder

Replace the path below if your project is stored somewhere else.

Copy and paste:

Check the current directory of source code :

```cmd
cd
```

List the files:

```cmd
dir
```

---

## 3. Check Python

Check that Python is installed:

```cmd
python --version
```

Check which Python executable is being used:

```cmd
where python
```

Check pip:

```cmd
python -m pip --version
```

---

## 4. Install / Update pip

Copy and paste:

```cmd
python -m pip install --upgrade pip
```

---

## 5. Check for Broken Dependencies

Run:

```cmd
python -m pip check
```

Expected result:

```text
No broken requirements found.
```

If pip reports dependency conflicts, resolve them before building the application.

---

## 6. Check Nuitka

Run:

```cmd
python -m nuitka --version
```

The requirements file specifies:

```text
4.1.3
```

---

## 7. Check Tkinter

Tkinter is part of the standard Windows Python installation and is not installed through the requirements file.

Run:

```cmd
python -c "import tkinter; print('Tkinter: OK')"
```

Expected result:

```text
Tkinter: OK
```

---

## 8. Check All Python Dependencies

Copy and paste this complete command:

```cmd
python -c "import tkinter, customtkinter, cryptography, PIL, arabic_reshaper; from bidi.algorithm import get_display; import nuitka; print('Tkinter: OK'); print('customtkinter:', customtkinter.__version__); print('cryptography:', cryptography.__version__); print('Pillow:', PIL.__version__); print('arabic-reshaper: OK'); print('python-bidi: OK'); print('Nuitka: OK')"
```

A successful environment should produce output similar to:

```text
Tkinter: OK
customtkinter: 6.0.0
cryptography: 49.0.0
Pillow: 12.3.0
arabic-reshaper: OK
python-bidi: OK
Nuitka: OK
```

---

## 9. Run the Python Source Directly

Before compiling, test the source itself.

Replace the Python filename below if your source file has a different name.

```cmd
python "Noble_password_manager_0.0.4.py"
```

If the filename contains spaces, keep the quotation marks.

---

## 10. Verify the Source Compiles

Run:

```cmd
python -m py_compile "Noble_password_manager_0.0.4.py"
```

If there is no output and CMD returns to the prompt, the Python source passed the syntax compilation check.

---

## 11. Check Installed Package Versions

You can inspect the installed packages with:

```cmd
python -m pip show arabic-reshaper
python -m pip show customtkinter
python -m pip show cryptography
python -m pip show Pillow
python -m pip show python-bidi
python -m pip show Nuitka
```

Or check all of them at once:

```cmd
python -m pip list
```

---

## 12. One-Command Environment Check

After installation, this command performs the main checks in one sequence:

```cmd
python --version && python -m pip --version && python -m pip check && python -m nuitka --version && python -c "import tkinter, customtkinter, cryptography, PIL, arabic_reshaper; from bidi.algorithm import get_display; print('ALL DEPENDENCIES OK')"
```

If that completes without errors, the main Python dependency environment is ready.

---

## 13. Optional: Create a Virtual Environment

Using a virtual environment is recommended for development and build isolation.

Create it:

```cmd
python -m venv .venv
```

Activate it:

```cmd
.venv\Scripts\activate
```

After activation, your prompt should show something similar to:

```text
(.venv) C:\Users\wwwni\Desktop\...
```

Then install the requirements:

```cmd
python -m pip install --upgrade pip
python -m pip install -r NoblePasswordManager_requirements.txt
```

Check the environment:

```cmd
python -m pip check
```

Deactivate when finished:

```cmd
deactivate
```

---

## 14. Recommended Build Preparation Sequence

Copy and paste the following commands one by one:

```cmd
cd "C:\Users\wwwni\Desktop\under develoment\password manager ( python tkinter )\Gemini versions\0.0.4\0.0.4"
```

```cmd
python --version
```

```cmd
where python
```

```cmd
python -m pip --version
```

```cmd
python -m pip install --upgrade pip
```

```cmd
python -m pip install -r NoblePasswordManager_requirements.txt
```

```cmd
python -m pip check
```

```cmd
python -c "import tkinter; print('Tkinter: OK')"
```

```cmd
python -m nuitka --version
```

```cmd
python -c "import customtkinter, cryptography, PIL, arabic_reshaper; from bidi.algorithm import get_display; print('customtkinter:', customtkinter.__version__); print('cryptography:', cryptography.__version__); print('Pillow:', PIL.__version__); print('arabic-reshaper: OK'); print('python-bidi: OK')"
```

```cmd
python -m py_compile "Noble_password_manager_0.0.4.py"
```

```cmd
python "Noble_password_manager_0.0.4.py"
```

---

## 15. Important Notes

### Tkinter

Tkinter is part of the standard Python installation on Windows. Do not add `tkinter` to the pip requirements file.

### Runtime vs Build Dependencies

The following packages are used by the application:

```text
arabic-reshaper
customtkinter
cryptography
Pillow
python-bidi
```

Nuitka is included because it is the compiler/build tool used to create the Windows executable.

### Version Pinning

The versions in the requirements file are pinned so that the intended environment is reproducible:

```text
arabic-reshaper==3.0.1
customtkinter==6.0.0
cryptography==49.0.0
Pillow==12.3.0
python-bidi==0.6.11
Nuitka==4.1.3
```

Do not change these versions casually when trying to reproduce an existing build.

### Existing Compilation Note

A previous Nuitka compilation environment for this project recorded Python 3.14.6 and Nuitka 4.1.3. That environment also used the Zig compiler. If Nuitka later fails during C/C++ linking, that can be a compiler/toolchain problem rather than a missing Python package.

---

## 16. Basic Troubleshooting

### `python is not recognized`

Check:

```cmd
where python
```

and:

```cmd
py --version
```

If `py` works but `python` does not, you can use:

```cmd
py -m pip --version
```

and:

```cmd
py -m pip install -r NoblePasswordManager_requirements.txt
```

### `No module named customtkinter`

Run:

```cmd
python -m pip install customtkinter==6.0.0
```

### `No module named cryptography`

Run:

```cmd
python -m pip install cryptography==49.0.0
```

### `No module named PIL`

Run:

```cmd
python -m pip install Pillow==12.3.0
```

### `No module named arabic_reshaper`

Run:

```cmd
python -m pip install arabic-reshaper==3.0.1
```

### `No module named bidi`

Run:

```cmd
python -m pip install python-bidi==0.6.11
```

### Check everything again

```cmd
python -m pip check
```

and:

```cmd
python -c "import tkinter, customtkinter, cryptography, PIL, arabic_reshaper; from bidi.algorithm import get_display; import nuitka; print('ALL DEPENDENCIES OK')"
```

---

## 17. Final Environment Verification

Before building a release, all of the following should work:

```cmd
python --version
```

```cmd
python -m pip --version
```

```cmd
python -m pip check
```

```cmd
python -m nuitka --version
```

```cmd
python -c "import tkinter; print('Tkinter: OK')"
```

```cmd
python -c "import customtkinter, cryptography, PIL, arabic_reshaper; from bidi.algorithm import get_display; print('ALL DEPENDENCIES OK')"
```

```cmd
python -m py_compile "Noble_password_manager_0.0.4.py"
```

Once these checks succeed, the Python environment is prepared for the next build step.
