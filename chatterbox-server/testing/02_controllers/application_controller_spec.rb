describe ApplicationController do
  let(:message1) { Message.first }
  let(:message2) { Message.second }

  before do
    Message.create(body: "Hello 👋", username: "Liza")
    Message.create(body: "Hi!", username: "Duane")
  end

  describe 'GET /messages' do
    it 'returns an array of JSON objects for all messages in the database' do
      get '/messages'

      expect(last_response.body).to include_json([
        { body: "Hello 👋", username: "Liza", created_at: message1.created_at.as_json },
        { body: "Hi!", username: "Duane", created_at: message2.created_at.as_json }
      ])
    end
  end

  describe 'POST /messages' do
    let(:params) do
      { body: "let's get this chat app working", username: "Liza" }
    end

    it 'creates a new message in the database' do
      expect { post "/messages", params }.to change(Message, :count).from(2).to(3)
    end

    it 'returns data for the newly created message as JSON' do
      post "/messages", params

      expect(last_response.body).to include_json(
        body: "let's get this chat app working", 
        username: "Liza"
      )
    end
  end

  describe 'PATCH /messages/:id' do
    let(:params) do
      { body: "Hi!!!!" }
    end

    it 'updates the body of the message in the database' do
      expect do 
        patch "/messages/#{message2.id}", params

        message2.reload
      end.to change(message2, :body).to("Hi!!!!")
    end

    it 'returns data for the updated message as JSON' do
      patch "/messages/#{message2.id}", params

      expect(last_response.body).to include_json(body: "Hi!!!!")
    end
  end

  describe 'DELETE /messages/:id' do
    it 'deletes the message from the database' do
      expect { delete "/messages/#{message2.id}" }.to change(Message, :count).from(2).to(1)
    end
  end

end
