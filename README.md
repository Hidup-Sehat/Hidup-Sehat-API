# HidupSehat API

The HidupSehat is a FastAPI-based API designed for mobile apps that focus on promoting a healthy lifestyle. Powered by machine learning, it offers seamless integration with Firebase Firestore. Can be accessed at 
[Here](https://apihidupsehat.my.id/docs).
## Usage/Examples

To use the HidupSehat API deployed on Cloud Run, follow these steps:

```
curl -X 'GET' \
  'https://apihidupsehat.my.id/v1/weekly-leaderboard' \
  -H 'accept: application/json'
```
The API will respond with the Weekly Leaderboard in JSON format. Here's an example response:
```
{
  "weekEndDate": "18-06-2023",
  "weekStartDate": "12-06-2023",
  "data": [
    {
      "user_uid": "buHJ6rChG0YTZi9FflGC7XZqEek2",
      "username": "Rijal Muhyidin",
      "name": "Rijal Muhyidin",
      "imgUrl": "https://firebasestorage.googleapis.com/v0/b/hidup-sehat-server.appspot.com/o/blank-profile.png?alt=media&token=416c3ef1-8c69-453c-b9c6-e35e390102b8&_gl=1*1z115oz*_ga*MjAzMzY5MDczOC4xNjg1MDM0NTY1*_ga_CW55HF8NVT*MTY4NjQxMTQyOC4yNC4xLjE2ODY0MTIyNjUuMC4wLjA.",
      "point": 20
    }
  ]
}
```
Explore the different API endpoints available for your use case. Refer to the [API documentation](https://apihidupsehat.my.id/docs) or [here](https://hidup-sehat-api-production.up.railway.app/docs) for more details on the available routes and request/response formats.
## Deployment

These are the step to deploy on Cloud Run:
1.  Make sure you join the **capstone-hidup-sehat** Google Cloud project
2.  Go to the [Cloud Run Section](https://console.cloud.google.com/run) in Google Cloud
3.  Click create service
4.  Click on Continuously deploy new revisions from a source repository and click on Set Up with Cloud Build
5.  Use github as source repository and choose **Hidup-Sehat/Hidup-Sehat-API** as the repository then click next
6.  Choose the branch and use Dockerfile as build type then just leave Source Location by default
7.  Change the Service name and the region as it should
8.  To avoid high billing, choose __CPU is only allocated during request processing__ and set the Minimum number of instances to __0__ and the Maximum number of instances to __5__. (You can set the maximum to around 5-10)
9.  Choose __All__ for Ingress Control
10. Set __Allow unauthenticated invocations__ to make our API public
11. Click create and wait
12. The project should be deployed
## Documentation

Here's the link to our [API Documentation](https://apihidupsehat.my.id/docs) or [here](https://hidup-sehat-api-production.up.railway.app/docs) automatically created by FastAPI.


## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Make sure you have Python and Pip installed locally

```bash
  python –version && pip --version
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Get the Environment Variables
```bash
  Contact Us
```

Start the server

```bash
  uvicorn app.main:app --reload
```

API should be started locally, access the backend via [http://localhost:8000](http://localhost:8000) and the docs via [http://localhost:8000](http://localhost:8000)
## Acknowledgements

We would like to acknowledge the following individuals and projects for their contributions to the development of the HidupSehat API:


- [FastAPI](https://fastapi.tiangolo.com/) The FastAPI framework provided a solid foundation for building the API.
- [Firebase Firestore](https://firebase.google.com/) Firebase Firestore enabled efficient data management and seamless integration with the HidupSehat API.
- [Docker](https://www.docker.com/) Docker made it easy to containerize the HidupSehat API for deployment on Cloud Run.
- [Readme.so](https://readme.so) & [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) for making it easy to create a beautiful README.md
- HidupSehat Team for putting on hardwork and efforts such to make this Capstone Project successful

