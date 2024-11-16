import { useState } from 'react'
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import { MainContainer, ChatContainer, MessageList, Message, MessageInput, TypingIndicator } from '@chatscope/chat-ui-kit-react';
import "../Chat.css"

const API_KEY = "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";

const systemMessage = { //  Explain things like you're talking to a software professional with 5 years of experience.
  "role": "system", "content": "Explain things like you're talking to a software professional with 2 years of experience."
}

function Tmp() {
  const [messages, setMessages] = useState([
    {
      message: "Hello, I'm ChatGPT! Ask me anything!",
      sentTime: "just now",
      sender: "ChatGPT"
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = async (message) => {
    const newMessage = {
      message,
      direction: 'outgoing',
      sender: "user"
    };

    const newMessages = [...messages, newMessage];
    setMessages(newMessages);

    setIsTyping(true);
    await processMessageToChatGPT(newMessages);
  };

  async function processMessageToChatGPT(chatMessages) {
    let apiMessages = chatMessages.map((messageObject) => {
      let role = "";
      if (messageObject.sender === "ChatGPT") {
        role = "assistant";
      } else {
        role = "user";
      }
      return { role: role, content: messageObject.message }
    });

    const apiRequestBody = {
      "model": "gpt-3.5-turbo",
      "messages": [
        systemMessage,
        ...apiMessages
      ]
    };

    await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(apiRequestBody)
    }).then((data) => {
      return data.json();
    }).then((data) => {
      setMessages([
        ...chatMessages,
        {
          message: data.choices[0].message.content,
          sender: "ChatGPT"
        }
      ]);
      setIsTyping(false);
    });
  }

  return (
    <div className="flex justify-center items-center h-screen relative overflow-hidden">
    <div className="relative h-[600px] w-[1000px] bg-orange-500 rounded-lg shadow-lg overflow-hidden msg-custom-section">
      
      <MainContainer className="main-container">
    <ChatContainer className="chat-container-new-look">
    <div className="chat-header">Chat with AI</div>    
    <MessageList
      scrollBehavior="smooth"
      typingIndicator={isTyping ? <TypingIndicator content="ChatGPT is typing" /> : null}
    >
      {messages.map((message, i) => {
        return (
          <div key={i} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} mb-3`}>
            <div
              className={`max-w-[80%] p-4 rounded-lg shadow-md transition-all duration-300 ${
                message.sender === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-800'
              }`}
            >
              {message.message}
            </div>
          </div>
        );
      })}
    </MessageList>
    <MessageInput
      placeholder="Type message here"
      onSend={handleSend}
      className="message-input"
    />
  </ChatContainer>
</MainContainer>

    </div>
  </div>
  )
}  
  
export default Tmp;
