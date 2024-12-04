import './App.css';
import { Amplify } from 'aws-amplify';
import { Authenticator, withAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import awsExports from './aws-exports';
import TextGenerationApp from './components/TextGenerationApp.js'; // Імпорт компонента

Amplify.configure(awsExports);

function App({ signOut, user }) {
  return (
    <div className="App">
      <header className="App-header">
        <Authenticator>
          {({ signOut, user }) => (
            <main>
              <div className="App">
                <header className="App-header">
                  <TextGenerationApp signOut={signOut} />
                </header>
              </div>
            </main>
          )}
        </Authenticator>
      </header>
    </div>
  );
}

export default withAuthenticator(App);
