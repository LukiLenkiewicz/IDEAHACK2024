import React, { useState, useEffect } from "react";
import axios from "axios";

const Chat = ({ room }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [user, setUser] = useState(() => {
    // Load user from localStorage or set default
    const savedUser = localStorage.getItem("authUser");
    return savedUser ? JSON.parse(savedUser).username || "Guest" : "Guest";
  });

  useEffect(() => {
    const feed = JSON.parse(localStorage.getItem("authUser"));

    const fetchMessages = async () => {
      try {
        const response = await axios.post(
          `http://localhost:8000/api/chat/${feed.type}/${feed.id}`,
          { query: "Fetch messages" } // Sending a generic query to comply with the backend structure
        );
        setMessages(response.data.messages || []);
      } catch (err) {
        console.error("Error fetching messages:", err);
      }
    };

    // Initial fetch
    fetchMessages();

    // Poll every 3 seconds to simulate real-time updates
    const interval = setInterval(fetchMessages, 3000);
    return () => clearInterval(interval); // Cleanup on component unmount
  }, [room]);

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!newMessage.trim()) return;

    try {

      // Send the new message to the backend
      const response = await axios.post(
        `http://localhost:8000/api/chat/`,
        {
          query: newMessage,
        }
      );

      // Update messages locally
      setMessages((prevMessages) => [
        ...prevMessages,
        { id: Date.now(), user, text: newMessage }, // Add the new message to local state
      ]);
      setNewMessage(""); // Clear input
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
        {messages.map((message, index) => (
          <div key={index} className="flex items-start mb-3">
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
          className="flex-1 border p-2 rounded-l-lg"
          placeholder="Type your message here..."
        />
        <button
          type="submit"
          className="bg-[#3b5998] text-white px-4 py-2 rounded-r-lg"
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
  const [authUser, setAuthUser] = useState(() => {
    // Load user from localStorage or set default
    return localStorage.getItem("authUser")
      ? JSON.parse(localStorage.getItem("authUser"))
      : { username: "Guest", type: "default", id: 0 };
  });

  return (
    <div className="App">
      {!isInChat ? (
        <div className="room">
          <label className="block mb-2">Enter Room Name:</label>
          <input
            onChange={(e) => setRoom(e.target.value)}
            className="border p-2 mb-2"
          />
          <button
            onClick={() => {
              if (room.trim()) {
                setIsInChat(true);
                // Optionally, save authUser to localStorage here
                localStorage.setItem(
                  "authUser",
                  JSON.stringify({ ...authUser, room })
                );
              }
            }}
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
