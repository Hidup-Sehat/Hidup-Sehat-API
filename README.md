<p align="center">
  <img src="https://raw.githubusercontent.com/Hidup-Sehat/.github/main/profile/Horizontal%20Logo-whitebg.png" alt="Hidup Sehat Logo">
  <h1 align="center">HidupSehat</h1>
  <p align="center">HidupSehat is Innovative All-in-One Healthy Lifestyle Mobile Application</p>
</p>

# ❓ HidupSehat API

The HidupSehat is a FastAPI-based API designed for mobile apps that focus on promoting a healthy lifestyle. Offers seamless integration with Firebase Firestore and Powered by machine learning. Can be accessed at
[Here](https://hidup-sehat-api-oppougulda-as.a.run.app).

## 📚 Usage/Examples

To use the HidupSehat API deployed on Cloud Run, follow these steps:

```bash
curl -X 'GET' \
  'https://hidup-sehat-api-oppougulda-as.a.run.app/v1/weekly-leaderboard' \
  -H 'accept: application/json'
```

The API will respond with the Weekly Leaderboard in JSON format. Here's an example response:

```json
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

Explore the different API endpoints available for your use case. Refer to the [API documentation](https://hidup-sehat-api-oppougulda-as.a.run.app/docs) or [here](https://hidup-sehat-api-production.up.railway.app/docs) for more details on the available routes and request/response formats.

## ⚡ Features (API)

⚡ Sign Up and Login\
⚡ Machine Learning Powered Article Feeds\
⚡ Health Monitoring\
⚡ Food Detection and Nutrition Information\
⚡ Food History with Calorie Tracker\
⚡ Diary and Journal\
⚡ Yoga Pose Detection\
⚡ Leaderboard\
⚡ Calorie, Water, and Sleep Tracker

## 🚀 How we Deploy it in < 5 Minute

![hero](https://firebasestorage.googleapis.com/v0/b/hidup-sehat-server.appspot.com/o/cloudrun_deploy.png?alt=media&token=eb8efece-d119-48db-b948-a2a6517bf25a)
These are the step to deploy on Cloud Run:

1.  Make sure you join the **capstone-hidup-sehat** Google Cloud project (or using your own project)
2.  Go to the [Cloud Run Section](https://console.cloud.google.com/run) in Google Cloud
3.  Click **Create Service**
4.  Click on **Continuously deploy new revisions from a source repository** and click on **Set Up with Cloud Build**
5.  Use github as source repository and choose **Hidup-Sehat/Hidup-Sehat-API** as the repository then click next
6.  **Choose the branch** and use **Dockerfile** as build type then just leave Source Location by default
7.  Change the Service name and the region as it should
8.  To avoid high billing, choose **CPU is only allocated during request processing** and set the Minimum number of instances to **0** and the Maximum number of instances to **5**. (You can set the maximum to around 5-10)
9.  Choose **All** for Ingress Control
10. Set **Allow unauthenticated invocations** to make our API public
11. Configure **Environment Variables** as it should
12. Click create and wait
13. The project should be deployed

## 📖 Documentation

Visit [API Documentation](https://hidup-sehat-api-oppougulda-as.a.run.app/docs) or [here](https://hidup-sehat-api-production.up.railway.app/docs) to view the documentation, automatically created by FastAPI.

## 🛠️ Install & Run Locally

### Prerequisites

- Python 3.6+
- Pip
- Git

### Installation

Clone the project 📦

```bash
git clone https://github.com/Hidup-Sehat/Hidup-Sehat-API.git
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
Contact Us for the Environment Variables
```

### Run Locally

Start the server

```bash
uvicorn app.main:app --reload
```

API should be started locally, access the backend via http://localhost:8000 and the docs via http://localhost:8000/docs \
Note: Make sure you have the Environment Variables from us before trying it out.

## ❤️ Acknowledgements

We would like to acknowledge the following groups, individuals and projects for their contributions to the development of the HidupSehat API:

- [Bangkit Academy 2023](https://grow.google/intl/id_id/bangkit/) Who provide us with outstanding quality of Education
- [HidupSehat Team](https://github.com/Hidup-Sehat#our-teams) for putting on hardwork and efforts such to make this Capstone Project successful
- **Mentor** [Eric Julianto](twitter.com/algonacci) & [Adrianus Wicaksono](https://www.linkedin.com/in/chuck1z/) for their guidance and support on Cloud Run Deployment and API
- [FastAPI](https://fastapi.tiangolo.com/) The FastAPI framework provided a solid foundation for building the API.
- [Firebase Firestore](https://firebase.google.com/) Firebase Firestore enabled efficient data management and seamless integration with the HidupSehat API.
- [Docker](https://www.docker.com/) Docker made it easy to containerize the HidupSehat API for deployment on Cloud Run.
- [Readme.so](https://readme.so) & [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) for making it easy to create a beautiful README.md

## 💻 Hire the Authors!

**Edy Setiawan - Backend Engineer**\
Lead the Dockerization and Deployment on Cloud Run\
💬 [LinkedIn](https://www.linkedin.com/in/e-edsen/) [Github](https://github.com/e-edsen/) [Email](mailto:edy.setiawan213@gmail.com)

**I Wayan Natura Adnyana - Frontend Engineer**\
Lead the making of the API and Testing\
💬 [LinkedIn](https://www.linkedin.com/in/natura-adnyana/) [Github](https://github.com/NaturaAdnyana/)
[Email](mailto:natura538@gmail.com)

To ask questions, report bugs, asking for environment variables you can contact us too.

## 📝 License
