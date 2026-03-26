import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

function App() {
    const [message, setMessage] = useState("");
    const [chat, setChat] = useState([]);
    const [files, setFiles] = useState([]);
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [chat, isTyping]);

    const getTimeStamp = () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const sendMessage = async () => {
        if (!message.trim()) return;

        const currentMessage = message;
        setChat(prev => [...prev, { sender: "You", text: currentMessage, time: getTimeStamp() }]);
        setMessage("");
        setIsTyping(true);

        try {
            const res = await axios.post("http://127.0.0.1:5000/chat", { message: currentMessage });
            setChat(prev => [...prev, { sender: "Bot", text: res.data.response, time: getTimeStamp() }]);
        } catch (err) {
            console.error(err);
            setChat(prev => [...prev, { sender: "Bot", text: "Error in response from backend!", time: getTimeStamp() }]);
        } finally {
            setIsTyping(false);
        }
    };

    const handleFiles = async (e) => {
        const selectedFiles = Array.from(e.target.files);
        setFiles(selectedFiles);

        const formData = new FormData();
        selectedFiles.forEach(file => formData.append("files", file));

        try {
            await axios.post("http://127.0.0.1:5000/upload", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });
            setChat(prev => [...prev, { sender: "Bot", text: "Files uploaded successfully! Ready to answer questions about them.", time: getTimeStamp() }]);
        } catch (err) {
            console.error(err);
            alert("Error uploading files!");
        }
    };

    return (
        <div className="app-container">
            <div className="chat-header">My Chatgpt</div>

            <div className="chat-messages">
                {chat.map((c, i) => (
                    <div key={i} className={`message-row ${c.sender === "You" ? "user" : "bot"}`}>
                        <div className="message-content">
                            {c.sender === "Bot" && (
                                <div className="avatar bot-avatar">
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <polyline points="4 7 4 4 20 4 20 7"></polyline>
                                        <line x1="9" y1="20" x2="15" y2="20"></line>
                                        <line x1="12" y1="4" x2="12" y2="20"></line>
                                    </svg>
                                </div>
                            )}
                            {c.sender === "You" ? (
                                <div className="user-bubble">{c.text}</div>
                            ) : (
                                <div className="bot-bubble">{c.text}</div>
                            )}
                        </div>
                    </div>
                ))}
                {isTyping && (
                    <div className="message-row bot">
                        <div className="message-content">
                            <div className="avatar bot-avatar">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <polyline points="4 7 4 4 20 4 20 7"></polyline>
                                    <line x1="9" y1="20" x2="15" y2="20"></line>
                                    <line x1="12" y1="4" x2="12" y2="20"></line>
                                </svg>
                            </div>
                            <div className="bot-bubble">Typing...</div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="input-container">
                <div className="input-box">
                    <label className="upload-btn" title="Upload files">
                        <input type="file" multiple onChange={handleFiles} />
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" />
                        </svg>
                    </label>
                    <input
                        type="text"
                        value={message}
                        placeholder="Message ChatGPT..."
                        onChange={e => setMessage(e.target.value)}
                        onKeyDown={e => {
                            if (e.key === "Enter") {
                                sendMessage();
                            }
                        }}
                    />
                    <button className="send-btn" onClick={sendMessage} disabled={!message.trim()}>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <line x1="12" y1="19" x2="12" y2="5"></line>
                            <polyline points="5 12 12 5 19 12"></polyline>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    );
}

export default App;