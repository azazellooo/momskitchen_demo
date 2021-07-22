pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
       stage ("Get Latest Code") {
           steps {
                checkout scm
           }
       }

       stage ("Install Application Dependencies") {
            steps {
                sh '''
                source venv/bin/activate
                pip install -r requirements.txt
                deactivate
               '''
            }
       }
       stage ("Collect Static files") {
           steps {
              sh '''
                  source bin/activate
                  cd server
                  python manage.py collectstatic --noinput
                  deactivate
                 '''
           }
       }
       stage(build) {
          steps {
             echo 'Notify GitLab'
          }
       }
       stage(test) {
           steps {
               echo 'Notify GitLab'
           }
       }
    }
 }