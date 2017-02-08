try{
    stage 'Checkout SCMt'
    node{
        slackSend channel: '#builds', color: '#6699FF', message: 'Build Started: flask-template', teamDomain: 'skyone', tokenCredentialId: 'e4e45d53-edd1-4752-84dd-e8b222f5b02f'
        checkout scm
    }

    stage 'installing dependencies'
    node {
        sh '''
            virtualenv /opt/envs/flask_template
            /opt/envs/flask_template/bin/pip install -r resources/requirements.txt
        '''
    }

    stage 'Testing'
    node{
        sh '''
            /opt/envs/flask_template/bin/nosetests --cover-erase  --with-coverage --cover-package=flask_template --cover-html tests/unit_tests.py
            /opt/envs/flask_template/bin/nosetests --with-coverage --cover-package=flask_template --cover-html tests/integrated_tests.py   
            /opt/envs/flask_template/bin/coverage xml
            /opt/tools/sonar-runner-2.4/bin/sonar-runner
        '''
    }

    stage 'Publishing'
    node{
        sh '''
            echo "testing"
            #aws s3 sync angular/ s3://skysaver --acl public-read
        '''
        slackSend channel: '#builds', color: '#1CC36F', message: 'Build Finished: flask-template', teamDomain: 'skyone', tokenCredentialId: 'e4e45d53-edd1-4752-84dd-e8b222f5b02f'
    }
} catch(e){
    slackSend channel: '#builds', color: 'F04343', message: 'Build Failed: flask-template', teamDomain: 'skyone', tokenCredentialId: 'e4e45d53-edd1-4752-84dd-e8b222f5b02f'
    e.printStackTrace()
}

