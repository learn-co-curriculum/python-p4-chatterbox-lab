describe Message do
  let(:message) { Message.first }

  before do
    Message.create(body: "Hello 👋", username: "Liza")
  end
  
  it "has the correct columns in the messages table" do
    expect(message).to have_attributes(
      body: "Hello 👋", 
      username: "Liza", 
      created_at: a_kind_of(Time), 
      updated_at: a_kind_of(Time)
    )
  end
  
end
