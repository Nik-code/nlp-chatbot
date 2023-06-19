$(document).ready(function() {
    // chat form
    $('#chatbot-chat-form').submit(function(event) {
        event.preventDefault();
        var query = $('#chatbot-query-input').val();
        $('#chatbot-query-input').val('');
        sendQuery(query);
    });

    function sendQuery(query) {
        var url = '/query';
        var top5 = $('#toggleResponse').is(":checked");  // Check the checkbox value
        var data = JSON.stringify({ query: query, top5: top5 });  // Include the checkbox value in the request
        displayUserQuery(query);

        $.ajax({
            url: url,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: data,
            success: function(response) {
                displayResponse(response.response);
                displayBotMessage("I hope I was able to help you. If not, please contact the support team.");
                displayBotMessage("Do you have any other queries?");
            },
            error: function(xhr, status, error) {
                console.log('Error:', error);
            }
        });
    }


    function displayUserQuery(query) {
        var chatWindow = $('#chatbot-chat-window');
        var messageContainer = $('<div>').addClass('chat-container user');
        var message = $('<div>').addClass('chat-message').text(query);
        messageContainer.append(message);
        chatWindow.append(messageContainer);
        chatWindow.scrollTop(chatWindow[0].scrollHeight);
    }


    function displayBotMessage(to_show) {
        var chatWindow = $('#chatbot-chat-window');
        var messageContainer = $('<div>').addClass('chat-container bot');
        var to_show = $('<div>').addClass('chat-message').text(to_show);
        messageContainer.append(to_show);
        chatWindow.append(messageContainer);
        chatWindow.scrollTop(chatWindow[0].scrollHeight);
    }

    function displayResponse(responseList) {
        var chatWindow = $('#chatbot-chat-window');
        responseList.forEach(function (responseItem) {
            var query = responseItem[0];
            var response = responseItem[1];
            var score = responseItem[2];

            var messageContainer = $('<div>').addClass('chat-container bot');
            var message = $('<div>').addClass('chat-message').html(`
                <strong>Query:</strong> ${query}<br>
                <strong>Response:</strong> ${response}<br>
                <strong>Score:</strong> ${score}
            `);
            messageContainer.append(message);
            chatWindow.append(messageContainer);
        });
        chatWindow.scrollTop(chatWindow[0].scrollHeight);
    }

    // sidebar buttons
    $('#myinfo').click(function() {
        $('#infoCard').toggleClass('hidden');
    });

    $('#chatbot').click(function() {
        $('#chatbotCard').toggleClass('hidden');
    });

    $('#logout').click(function() {
        alert('Logout successful');
        window.location.href = '/logout';
    });
});
