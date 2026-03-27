import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Database, Globe, Layers } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';

const App = () => {
    const [messages, setMessages] = useState([
        { role: 'agent', content: '¡Hola! Soy tu Agente Universal MCP. He estudiado tu biblioteca en Portainer y estoy listo para ayudarte. ¿Qué quieres investigar hoy?' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [metaContext, setMetaContext] = useState(null);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(scrollToBottom, [messages]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage = input;
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await axios.post('/api/v1/chat', { message: userMessage });
            const data = response.data;

            setMessages(prev => [...prev, { role: 'agent', content: data.answer }]);
            setMetaContext(data.intent_plan);
        } catch (error) {
            setMessages(prev => [...prev, { role: 'error', content: 'Hubo un error al conectar con el servidor.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="app-container">
            {/* Sidebar - Meta Context Visualization */}
            <aside className="sidebar">
                <div className="logo">
                    <h2 style={{ fontSize: '1.25rem', color: 'var(--accent-color)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Layers size={24} /> Universal MCP
                    </h2>
                </div>

                <div className="context-panel">
                    <h3 style={{ fontSize: '0.85rem', textTransform: 'uppercase', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                        Meta-Contexto Activo
                    </h3>
                    {metaContext ? (
                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="context-card"
                            style={{ background: 'rgba(255,255,255,0.05)', padding: '1rem', borderRadius: '0.75rem', border: '1px solid var(--glass-border)' }}
                        >
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                                {metaContext.server === 'mongodb' ? <Database size={16} /> : <Globe size={16} />}
                                <span style={{ fontWeight: '600' }}>{metaContext.server || 'Qdrant'}</span>
                            </div>
                            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                                Acción: {metaContext.action} <br />
                                Herramienta: {metaContext.tool || 'Vector Search'}
                            </p>
                        </motion.div>
                    ) : (
                        <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Esperando análisis semántico...</p>
                    )}
                </div>
            </aside >

            {/* Main Chat Area */}
            < main className="main-chat" >
                <header style={{ padding: '1rem 2rem', borderBottom: '1px solid var(--glass-border)', background: 'rgba(255,255,255,0.02)' }}>
                    <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Interacción Directa con la Biblioteca</span>
                </header>

                <div className="chat-messages">
                    <AnimatePresence>
                        {messages.map((msg, i) => (
                            <motion.div
                                key={i}
                                className={`message ${msg.role}`}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                            >
                                <div style={{ display: 'flex', gap: '0.75rem' }}>
                                    {msg.role === 'agent' && <Bot size={20} style={{ color: 'var(--accent-color)' }} />}
                                    {msg.role === 'user' && <User size={20} />}
                                    <span>{msg.content}</span>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                    <div ref={messagesEndRef} />
                </div>

                <div className="input-area">
                    <div className="input-wrapper">
                        <input
                            type="text"
                            placeholder="Haz una pregunta a tu biblioteca..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                        />
                        <button className="send-btn" onClick={handleSend} disabled={isLoading}>
                            <Send size={20} />
                        </button>
                    </div>
                </div>
            </main >
        </div >
    );
};

export default App;
