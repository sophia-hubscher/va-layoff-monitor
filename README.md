# Virginia Layoff Monitor

Monitors Virginia's WARN notices for layoffs and sends an email alert when a new relevant layoff is detected

## Setup Instructions

### 1. **Add Your Company Name, Email, and App Password**

1. **Open the script file:**
   - Open `warn_alerter.py` in a text editor of your choice.

2. **Add your company name and email address:**
   - In the script, replace the values for the variables `COMPANY` and `EMAIL` with your tracked company name and your personal email address. Make sure that your value for the company name matches what you see on [the official WARN notice site](https://www.virginiaworks.gov/warn-notices/).

4. **Create and add your app password:**
   - **For Gmail**:  
     If you’re using Gmail, you’ll need to generate an app-specific password if 2-factor authentication (2FA) is enabled:
     - Go to your [Google account security settings](https://myaccount.google.com/security).
     - Search for **App passwords** in the top search bar and click the first result.
     - Generate a new app password and copy it.
     - Paste it into the script where `PASSWORD` is defined.
   - **For other email providers**:  
     If you’re not using Gmail, you’ll need to refer to your email provider’s documentation on how to generate an app password or configure SMTP settings for sending emails.

### 2. **What to Do If You Don’t Use Gmail**

1. **Locate the SMTP settings**:
   - Find the section of the script where SMTP server details are set up.

2. **Update the SMTP settings** for your provider:
   - For **Outlook**, the server is typically `smtp-mail.outlook.com` with port `587`.
   - For **Yahoo**, use `smtp.mail.yahoo.com` with port `465`.
   - For other providers, refer to their SMTP documentation for details.

3. **Replace the credentials**:
   - Ensure your email address and app password are correctly inserted for the provider.

### 3. **Set Up a Cron Job for Automatic Weekly Execution**

To automatically run the script every week, you can set up a cron job on your system. Follow these steps:

1. **Make your script executable**:
   - In your terminal, navigate to the directory where the script is located, and make it executable:
     ```bash
     chmod +x /path/to/warn_alerter.py
     ```

2. **Create a Shell Script** (optional but recommended):
   - Create a new shell script (e.g., `run_warn_alerter.sh`) that activates your virtual environment (if used) and runs the Python script:
     ```bash
     #!/bin/bash
     source /path/to/your/venv/bin/activate
     python3 /path/to/warn_alerter.py
     ```

   - Make it executable:
     ```bash
     chmod +x /path/to/run_warn_alerter.sh
     ```

3. **Set up a Cron Job**:
   - Open your crontab file for editing:
     ```bash
     crontab -e
     ```

   - Add the following line to run your script every Monday at 9:00 AM:
     ```
     0 9 * * 1 /path/to/run_warn_alerter.sh >> /path/to/log.txt 2>&1
     ```
   - This will log the output and errors to `log.txt` and run the script at the specified time.

4. **Save and exit**:

### 4. **Check Logs for Script Output**

If you want to monitor the execution of your script, check the logs after it runs:
```bash
cat /path/to/log.txt
```
