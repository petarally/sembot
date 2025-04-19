document.addEventListener("DOMContentLoaded", function () {
  const chatForm = document.getElementById("chatForm");
  const userInput = document.getElementById("userInput");
  const chatMessages = document.getElementById("chatMessages");
  const suggestionButtons = document.querySelectorAll(".suggestion-btn");

  // Backend API URL
  const API_URL = "http://localhost:8000/api/chat";

  // Slušač događaja za slanje poruke
  chatForm.addEventListener("submit", function (e) {
    e.preventDefault();
    sendMessage(userInput.value);
  });

  // Slušači događaja za gumbe s prijedlozima
  suggestionButtons.forEach((button) => {
    button.addEventListener("click", function () {
      sendMessage(this.textContent);
    });
  });

  // Funkcija za slanje poruke
  function sendMessage(message) {
    if (!message.trim()) return;

    // Dodaj korisničku poruku u chat
    addMessage(message, "user");

    // Resetiraj input polje
    userInput.value = "";

    // Prikaži indikator učitavanja
    const loadingMessage = addMessage(
      "Učitavanje...",
      "bot",
      "loading-message"
    );

    // Pošalji zahtjev na API
    fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: message }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Ukloni indikator učitavanja
        chatMessages.removeChild(loadingMessage);

        // Dodaj odgovor bota
        addMessage(data.answer, "bot");
      })
      .catch((error) => {
        // Ukloni indikator učitavanja
        chatMessages.removeChild(loadingMessage);

        // Prikaži poruku o grešci
        addMessage(
          "Žao mi je, došlo je do greške prilikom obrade vašeg upita. Molimo pokušajte ponovno.",
          "bot"
        );
        console.error("Error:", error);
      });
  }

  // Funkcija za dodavanje poruke u chat
  function addMessage(content, sender, className = "") {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender} ${className}`;

    const messageContent = document.createElement("div");
    messageContent.className = "message-content";

    // Format URLs, emails and phone numbers as links
    if (sender === "bot") {
      // Format links (http/https URLs)
      content = content.replace(
        /(https?:\/\/[^\s]+)/g,
        '<a href="$1" target="_blank" rel="noopener">$1</a>'
      );

      // Format email addresses
      content = content.replace(
        /([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+)/g,
        '<a href="mailto:$1">$1</a>'
      );

      // Format phone numbers (simple pattern)
      content = content.replace(
        /(\+\d{1,3}\s?)?(\(?\d{3,5}\)?[\s.-]?\d{3}[\s.-]?\d{3,4})/g,
        '<a href="tel:$1$2">$&</a>'
      );

      // Use innerHTML for bot messages with formatted links
      messageContent.innerHTML = content;
    } else {
      // Use textContent for user messages (safer)
      messageContent.textContent = content;
    }

    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);

    // Scroll do najnovije poruke
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return messageDiv;
  }
});
