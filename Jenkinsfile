pipeline {
    agent any
    stages {
       stage ("Get Latest Code") {
           steps {
                checkout scm
           }
       }

       stage ("Install Application Dependencies") {
            steps {
                sh '''
                . venv/bin/activate
                pip install -r requirements.txt
                deactivate
               '''
            }
       }
       stage ("Collect Static files") {
           steps {
              sh '''
                  . venv/bin/activate
                  cd server
                  python manage.py collectstatic --noinput
                  deactivate
                 '''
           }
       }
       stage("build") {
          steps {
             echo 'Notify GitLab'
          }
       }
       stage("test") {
           steps {
                sh '''
               echo 'Notify GitLab'
               . venv/bin/activate
               cd server
               python manage.py makemigrations
               python manage.py migrate
               python manage.py test
               '''
           }
       }
    }
 }
