import React, { useState } from 'react';
import axios from 'axios';
import './styles/style.css';

function TextGenerationApp({ signOut }) {
    const [input, setInput] = useState('');
    const [output, setOutput] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleGenerate = async () => {
        setIsLoading(true);
        setError(null);
        setOutput(null);
        try {
            const formData = new FormData();
            formData.append('file', new Blob([input], { type: 'text/plain' }), 'input.txt');

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

    const handleInsertOutput = () => {
        if (output && output.text) {
            setInput(output.text); // Вставка тексту output у textarea
        }
    };

    return (
        <div className="app">
            <div className="header">
                <button className="sign-out-button" onClick={signOut}>Sign out</button>
            </div>
            <div className="container">
                <div className="content">
                    <div className="textarea-container">
                        <textarea
                            className="textarea"
                            placeholder="Common sense questions and answers"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                        />
                        <div className="button-group">
                            <button
                                onClick={handleGenerate}
                                disabled={isLoading}
                                className={`generate-button ${isLoading ? 'disabled' : ''}`}
                            >
                                {isLoading ? 'Generating...' : 'Generate'}
                            </button>
                        </div>
                    </div>
                    <div className="output-container">
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
