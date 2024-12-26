# Instagram Unfollower 🙅‍♂️📉

A simple **Streamlit app** to help you identify the people on Instagram who don't follow you back! This project is designed to help you manage your Instagram following list, clearing out the accounts that don’t reciprocate your follow and letting you focus on people who genuinely care about your content. 💖

---

## 🚀 Features
- **Upload Instagram data**: Upload the ZIP file you downloaded from Instagram's Account Center.
- **Unfollowers list**: The app identifies and displays the accounts you follow but who don't follow you back.
- **Interactive and user-friendly**: See your results with a clean and intuitive interface.
- **Privacy first**: All processing happens locally—your data is safe!

---

## 🛠 How It Works
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

---

## 📋 Requirements
To run this project, you need:
- Python 3.7+
- Streamlit
- BeautifulSoup4

Install the dependencies with:
```bash
pip install -r requirements.txt
```