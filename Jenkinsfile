pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
       stage ("Get Latest Code") {
            checkout scm
       }

       stage ("Install Application Dependencies") {
            sh '''
                source venv/bin/activate
                pip install -r requirements.txt
                deactivate
               '''
       }
       stage ("Collect Static files") {
          sh '''
              source bin/activate
              cd server
              python manage.py collectstatic --noinput
              deactivate
             '''
       }
       stage(build) {
          steps {
             echo 'Notify GitLab'
             updateGitlabCommitStatus name: 'build', state: 'pending'
             echo 'build step goes here'

             updateGitlabCommitStatus name: 'build', state: 'success'
          }
       }
       stage(test) {
           steps {
               echo 'Notify GitLab'
               updateGitlabCommitStatus name: 'test', state: 'pending'
               echo 'test step goes here'
               updateGitlabCommitStatus name: 'test', state: 'success'

           }
       }
    }
 }