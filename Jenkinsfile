pipeline {
  agent any
  stages {
    stage('build') {
      agent any
      environment {
        ARCH = 'x86_64'
        OS = 'sl7'
      }
      steps {
        sh 'echo "hi"'
      }
    }
    stage('Test') {
      steps {
        sh 'echo "test'
      }
    }
    stage('deploy') {
      steps {
        sh 'echo "deploy"'
      }
    }
  }
  environment {
    OS = 'sl7'
  }
}