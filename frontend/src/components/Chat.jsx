import { useState } from 'react'
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import { MainContainer, ChatContainer, MessageList, Message, MessageInput, TypingIndicator } from '@chatscope/chat-ui-kit-react';
import "../Chat.css"
import { Link, useNavigate } from 'react-router-dom';

function Tmp() {

  const navigate = useNavigate();
  const [messages, setMessages] = useState([
    {
      message: "Let's create your account, Tell me more about yourself ! :)",
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
      "message": chatMessages[chatMessages.length - 1].message  // Send last message to Django
    };

    try {
      const authUser = JSON.parse(localStorage.getItem("authUser"));
      const requestBody = {
        authUser,            // Include the authentication user data
        apiRequestBody       // Include the API request payload
      };

      
      const response = await fetch('http://localhost:8000/api/chatgpt/', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody)
      });

      const data = await response.json();
      console.log(response)
      if (response.ok && response.status !== 201) {

        // Add ChatGPT's response to the messages
        setMessages([
          ...chatMessages,
          {
            message: data.message,
            sender: "ChatGPT"
          }
        ]);
      } else if (response.status === 201) {
        console.log("HEjooo")
        navigate('/')
      }
      else {
        // Handle error response from Django backend
        console.error("Error:", data.error);
      }
    } catch (error) {
      console.error("An error occurred:", error);
    } finally {
      setIsTyping(false);
    }
  };

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
