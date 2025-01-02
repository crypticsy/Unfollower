# Unfollower 🙅‍♂️📉

A simple **Streamlit app** to help you identify the people on platforms who don't follow you back! This project is designed to help you manage your  following list, clearing out the accounts that don’t reciprocate your follow and letting you focus on people who genuinely care about your content. 💖

For now the app only supports Instagram and GitHub, but I plan to add more social media platforms in the future. Stay tuned! 🚀

<br/>

## 🚀 Features
- **Privacy first**: All processing happens locally—your data is safe!
- **Interactive and user-friendly**: See your results with a clean and intuitive interface.

<br/>

## 🛠 How It Works for Instagram
1. **Download your Instagram data**:
   - Log in to your Instagram account.
   - Go to **Meta Account Center > Privacy > Download Your Information**.
   - Request your data for **Followers and Following** in HTML format.
   - You'll receive an email from Instagram with a ZIP file link—download it.

2. **Upload your data to the app**:
   - Extract the ZIP file.
   - Upload the files containing **followers** and **following** information into the app.

3. **View the results**:
   - The app will compare your **following** list to your **followers** list.
   - It will show you the accounts that don't follow you back.

4. **Take action**:
   - Use the results to manage your following list directly in the Instagram app.

<br/>

## 📋 Requirements
To run this project by yourself, you need:
- Python 3.7+

Install the dependencies with:

```bash
pip install -r requirements.txt
```