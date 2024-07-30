# AI-Assisted Content Generation and Analysis

### Video Demo Link:
https://www.loom.com/share/6a788b901aa044eda30d1853385c97f6?sid=448dec17-76b5-45ca-9b9c-ce50be8b6f8a

Here's a guide on how to build this project on Google Cloud:

1. Create a new Google Cloud project
   
2. Enable following APIs:
   - Cloud Run Admin API
   - Cloud Build API
   - Vertex AI API  
3. Run the following command on Cloud Shell:
   
   ```
   gcloud config set project YOUR_PROJECT_ID
   ```

4. Clone the repository using the following command:
   
   ```
   git clone https://github.com/NehaKoppikar/ContentGenerationAnalysis.git
   ```

5. Change the working directory using the following command:
 
   ```
   cd ContentGeneratorAnalysis
   ```

6. Build Docker image
   
   ```
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/gen-analyzer
   ```

7. Deploy the image to Cloud Run

   ```
   gcloud run deploy --image gcr.io/YOUR_PROJECT_ID/gen-analyzer --platform managed
   ```
