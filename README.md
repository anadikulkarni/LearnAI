Follow the steps below to set up and run the application.

## Backend Setup

1. **Install Dependencies**  
   Navigate to the `code` directory and install the required Python packages:  
   `cd soft-engg-project-may-2024-se-team-1\Milestone 6\code`  
   `pip install -r new_requirements.txt`

2. **Delete Existing Database**  
   If a previous version of `seek_app.db` exists, delete it from the `code` directory to avoid conflicts.

3. **Populate the Database**  
   Create the database and populate it with initial data:  
   `python populate_data.py`
   This will create a new `seek_app.db` file.

5. **Run Flask**  
   Run the Flask application to get server live on localhost:  
   `flask run`  
   
## Frontend Setup

1. **Install Frontend Dependencies**  
   Navigate to the `Frontend` directory and install the required npm packages:  
   `cd soft-engg-project-may-2024-se-team-1\Milestone 6\code\frontend`  
   `npm install`

2. **Run the Frontend Development Server**  
   Start the frontend development server:  
   `npm run dev`  
   The frontend should now be running and accessible in your browser.

## GenAI Setup

### Prerequisites

The GenAI features of this project will only function if Ollama is installed and running locally. We recommend using the `gemma2:2b` model for optimal performance.

### Installing and Running Ollama

#### Windows

1. **Download Ollama**  
   Visit the [Ollama website](https://ollama.com/download) and download the Windows installer.

2. **Install Ollama**  
   Run the installer and follow the on-screen instructions to complete the installation.

3. **Run Ollama**  
   Once installed, open Command Prompt or PowerShell and run the following command to start Ollama:  
   ```bash
   ollama start
   ```

4. **Load Gemma2:2b Model**  
   To load the `gemma2:2b` model, execute the following command:  
   ```bash
   ollama run gemma2:2b
   ```

#### macOS

1. **Download Ollama**  
   Visit the [Ollama website](https://ollama.com/download) and download the macOS installer.

2. **Install Ollama**  
   Open the downloaded `.dmg` file and drag the Ollama application to your Applications folder.

3. **Run Ollama**  
   Open Terminal and start Ollama with the following command:  
   ```bash
   ollama start
   ```

4. **Load Gemma2:2b Model**  
   Load the `gemma2:2b` model by running the following command in Terminal:  
   ```bash
   ollama run gemma2:2b
   ```

#### Linux

1. **Install Ollama**  
   Ollama provides a Linux binary that can be downloaded from their [website](https://ollama.com/download). Alternatively, use `curl` to download and install it directly:  
   ```bash
   curl -LO https://ollama.com/download/linux/ollama_latest_amd64.deb
   sudo dpkg -i ollama_latest_amd64.deb
   ```

2. **Run Ollama**  
   Start Ollama by running the following command in your terminal:  
   ```bash
   ollama start
   ```

3. **Load Gemma2:2b Model**  
   Use the following command to load the `gemma2:2b` model:  
   ```bash
   ollama run gemma2:2b
   ```




## Notes

- Ensure that the backend is running before starting the frontend.
- For any issues, ensure all dependencies are correctly installed and that the database is properly set up.
- Ensure that Ollama is running before you start the backend of this project. If Ollama is not running, the GenAI features will not be available.
- For optimal performance, keep Ollama running throughout your development session.
- In case of issues with model loading, verify your internet connection as Ollama might need to download the `gemma2:2b` model initially.
