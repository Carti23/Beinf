import React, { useState } from 'react';
import axios from 'axios';
import './styles/style.css';

function TextGenerationApp({ signOut }) {
    const [input, setInput] = useState('');
    const [output, setOutput] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [tokenCount, setTokenCount] = useState(200);
    const [outputFormat, setOutputFormat] = useState('raw');

    const handleGenerate = async () => {
        setIsLoading(true);
        setError(null);
        setOutput(null);
        try {
            const formData = new FormData();
            formData.append('file', new Blob([input], { type: 'text/plain' }), 'input.txt');
            formData.append('tokenCount', tokenCount);
            formData.append('format', outputFormat);

            const response = await axios.post('http://0.0.0.0:8000/api/v1/generate/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            await waitForCompletion(response.data.id);
        } catch (error) {
            console.error('Error:', error);
            setError(error.message);
        } finally {
            setIsLoading(false);
        }
    };

    const waitForCompletion = async (id) => {
        while (true) {
            try {
                const outputResponse = await axios.get(`http://0.0.0.0:8000/api/v1/output/${id}`);
                if (outputResponse.data.status === 'done') {
                    setOutput(outputResponse.data);
                    break;
                }
                await new Promise(resolve => setTimeout(resolve, 5000)); // Wait for 5 seconds before next check
            } catch (error) {
                console.error('Error fetching output:', error);
                setError(error.message);
                break;
            }
        }
    };

    const handleStop = async () => {
        try {
            await axios.post('http://0.0.0.0:8000/stop/');
        } catch (error) {
            console.error('Error stopping generation:', error);
        }
    };

    const handleContinue = async () => {
        try {
            const response = await axios.post('http://0.0.0.0:8000/continue/');
            setOutput(response.data);
        } catch (error) {
            console.error('Error continuing generation:', error);
        }
    };

    const handleCountTokens = async () => {
        try {
            const response = await axios.post('http://0.0.0.0:8000/count_tokens/', { text: input });
            setTokenCount(response.data.count);
        } catch (error) {
            console.error('Error counting tokens:', error);
        }
    };

    return (
        <div className="app">
            <div className="header">
              <button className="sign-out-button" onClick={signOut}>Sign out</button>
            </div>
            <div className="container">
                <div className="tab-buttons">
                    {['Text generation', 'Parameters', 'Model', 'Training', 'Session'].map((tab) => (
                        <button key={tab} className="tab-button">{tab}</button>
                    ))}
                </div>

                <div className="content">
                    <div className="textarea-container">
                        <textarea
                            className="textarea"
                            placeholder="Common sense questions and answers"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                        />

                        <div className="token-controls">
                            <input
                                type="number"
                                value={tokenCount}
                                onChange={(e) => setTokenCount(e.target.value)}
                                className="token-input"
                            />
                            <div className="token-bar" />
                        </div>

                        <div className="button-group">
                            <button
                                onClick={handleGenerate}
                                disabled={isLoading}
                                className={`generate-button ${isLoading ? 'disabled' : ''}`}
                            >
                                {isLoading ? 'Generating...' : 'Generate'}
                            </button>
                            <button onClick={handleStop} className="stop-button">Stop</button>
                            <button onClick={handleContinue} className="continue-button">Continue</button>
                            <button onClick={handleCountTokens} className="count-tokens-button">Count tokens</button>
                        </div>
                    </div>

                    <div className="output-container">
                        <div className="format-buttons">
                            {['Raw', 'Markdown', 'HTML'].map((format) => (
                                <button
                                    key={format}
                                    onClick={() => setOutputFormat(format.toLowerCase())}
                                    className={`format-button ${outputFormat === format.toLowerCase() ? 'active' : ''}`}
                                >
                                    {format}
                                </button>
                            ))}
                        </div>
                        <div className="output-box">
                            {error ? (
                                <div style={{ color: '#e74c3c' }}>{error}</div>
                            ) : isLoading ? (
                                <p>Processing... Please wait.</p>
                            ) : output ? (
                                <div>
                                    <p>ID: {output.id}</p>
                                    <p>Link: {output.link}</p>
                                    <p>Text:</p>
                                    <pre style={{ margin: '0', whiteSpace: 'pre-wrap' }}>
                                        {output.text}
                                    </pre>
                                    <p>Status: {output.status}</p>
                                </div>
                            ) : (
                                <p>Click 'Generate' to start processing.</p>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default TextGenerationApp;