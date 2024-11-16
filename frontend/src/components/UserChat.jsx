import React, { useState, useEffect } from "react";
import axios from "axios";


const Chat = ({ room }) => {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState("");
    const [user, setUser] = useState("Guest");
  
    useEffect(() => {
      const fetchMessages = async () => {
        try {
          const response = await axios.get(`http://localhost:8000/api/messages/${room}/`);
          setMessages(response.data);
        } catch (err) {
          console.error("Error fetching messages:", err);
        }
      };
  
      fetchMessages();
    }, [room]);
  
    const handleSubmit = async (event) => {
      event.preventDefault();
  
      if (newMessage === "") return;
  
      try {
        await axios.post("http://localhost:8000/api/messages/", {
          text: newMessage,
          user,
          room,
        });
        setNewMessage("");
        const response = await axios.get(`http://localhost:8000/api/messages/${room}/`);
        setMessages(response.data);
      } catch (err) {
        console.error("Error sending message:", err);
      }
    };
  
    return (
      <div className="flex flex-col items-center w-[90%] mx-auto rounded-lg overflow-hidden border-2 border-[#3b5998]">
        <div className="bg-[#3b5998] text-white w-full text-center py-3">
          <h1>Welcome to: {room.toUpperCase()}</h1>
        </div>
        <div className="flex flex-col items-start w-full h-[80%] overflow-y-auto p-3 mb-3">
          {messages.map((message) => (
            <div key={message.id} className="flex items-start mb-3">
              <span className="font-bold text-[#333] mr-3">{message.user}:</span>
              {message.text}
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="flex w-full p-3">
          <input
            type="text"
            value={newMessage}
            onChange={(event) => setNewMessage(event.target.value)}
            className="flex-1 border-none outline-none bg-transparent text-[#333] text-lg p-2 rounded-l-lg"
            placeholder="Type your message here..."
          />
          <button
            type="submit"
            className="border-none outline-none bg-[#3b5998] text-white text-lg font-bold p-2 rounded-r-lg"
          >
            Send
          </button>
        </form>
      </div>
    );
  };
  
  function ChatApp() {
    const [isInChat, setIsInChat] = useState(false);
    const [room, setRoom] = useState("");
  
    return (
      <div className="App">
        {!isInChat ? (
          <div className="room">
            <label className="block mb-2">Type room name:</label>
            <input
              onChange={(e) => setRoom(e.target.value)}
              className="border p-2 mb-2"
            />
            <button
              onClick={() => setIsInChat(true)}
              className="bg-[#3b5998] text-white px-4 py-2 rounded"
            >
              Enter Chat
            </button>
          </div>
        ) : (
          <Chat room={room} />
        )}
      </div>
    );
  }
  
  export default ChatApp;
  