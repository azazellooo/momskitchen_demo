pipeline {
    agent any
    stages {
       stage ("Get Latest Code") {
            checkout scm
       }

       stage ("Install Application Dependencies") {
            sh '''
                source bin/activate
                pip install -r <relative path to requirements file>
                deactivate
               '''
       }
       stage ("Collect Static files") {
          sh '''
              source bin/activate
              python <relative path to manage.py> collectstatic --noinput
              deactivate
             '''
       }
       stage('build') {
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