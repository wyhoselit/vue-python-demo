<template>
  <v-container>
    <v-card>
      <v-card-title>AI Chat</v-card-title>
      <v-card-text>
        <div class="chat-history" style="height: 300px; overflow-y: auto;">
          <div v-for="message in messages" :key="message.id">
            <strong>{{ message.role }}:</strong> {{ message.text }}
          </div>
        </div>
        <v-text-field
          v-model="newMessage"
          @keyup.enter="sendMessage"
          label="Type a message..."
        />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const messages = ref<{id: number, role: string, text: string}[]>([]);
const newMessage = ref('');

const sendMessage = async () => {
  if (!newMessage.value) return;
  const userMessage = {id: Date.now(), role: 'user', text: newMessage.value};
  messages.value.push(userMessage);
  
  const response = await fetch('/api/v1/ai/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      messages: messages.value.map(m => ({role: m.role, content: m.text})),
      model: 'gpt-3.5-turbo',
      stream: true
    })
  });

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();
  
  messages.value.push({id: Date.now() + 1, role: 'assistant', text: ''});
  const assistantMessageIndex = messages.value.length - 1;

  while (true) {
    const {done, value} = await reader!.read();
    if (done) break;
    const chunk = decoder.decode(value);
    const data = JSON.parse(chunk);
    messages.value[assistantMessageIndex].text += data.choices[0].delta.content;
  }
  
  newMessage.value = '';
};
</script>
