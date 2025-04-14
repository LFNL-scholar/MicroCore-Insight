<template>
  <div class="chat-history-container">
    <div class="header">
      <button class="back-btn" @click="handleBack">
        <span class="arrow">←</span>
        返回
      </button>
      <h2 class="page-title">历史对话</h2>
    </div>

    <div class="chat-layout">
      <!-- 左侧对话列表 -->
      <div class="chat-list-panel">
        <div class="panel-header">
          <div class="search-box">
            <input type="text" placeholder="搜索对话..." v-model="searchText">
          </div>
        </div>
        <div class="conversation-list">
          <div v-if="isLoading" class="loading-state">
            加载中...
          </div>
          <div v-else-if="error" class="error-message">
            {{ error }}
            <button class="retry-button" @click="loadChatHistory">重试</button>
          </div>
          <div v-else-if="noChats" class="no-chats-message">
            暂无对话记录
          </div>
          <template v-else>
            <div v-for="group in groupedChats" :key="group.date" class="date-group">
              <div class="date-label">{{ group.date }}</div>
              <div 
                v-for="chat in group.chats" 
                :key="chat.id" 
                class="conversation-item"
                :class="{ active: selectedChat?.id === chat.id }"
                @click="selectChat(chat)"
              >
                <div class="conversation-time">{{ formatTime(chat.created_at) }}</div>
                <div class="preview-message">
                  {{ chat.title || '未命名对话' }}
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>

      <!-- 右侧聊天内容 -->
      <div class="chat-content-panel">
        <template v-if="selectedChat">
          <div class="panel-header">
            <span class="chat-time">{{ formatDateTime(selectedChat.created_at) }}</span>
            <span class="session-id">会话ID: {{ selectedChat.session_id }}</span>
          </div>
          <div class="messages-container">
            <template v-for="(message, index) in selectedChat.messages" :key="index">
              <div class="message-wrapper" :class="{ 'user-message-wrapper': message.role === 'user' }">
                <div class="message" :class="message.role === 'user' ? 'user-message' : 'assistant-message'">
                  <div class="message-content">{{ message.content }}</div>
                  <div class="message-footer">
                    <span v-if="message.role === 'assistant'" class="ai-label">AI生成</span>
                    <span class="message-time">{{ formatTime(message.time) }}</span>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </template>
        <div v-else class="empty-chat">
          <div class="empty-icon">💬</div>
          <p>请选择左侧对话查看详细内容</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getDeviceChatHistory } from '../api/device'

export default {
  name: 'ChatHistoryPage',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const deviceId = route.params.deviceId
    const searchText = ref('')
    const selectedChat = ref(null)
    
    const chatHistory = ref([])
    const isLoading = ref(true)
    const error = ref('')
    const noChats = ref(false)

    // 按日期对聊天记录进行分组
    const groupedChats = computed(() => {
      const filtered = searchText.value
        ? chatHistory.value.filter(chat => 
            chat.messages.some(msg => 
              msg.content.toLowerCase().includes(searchText.value.toLowerCase())
            )
          )
        : chatHistory.value

      const groups = {}
      filtered.forEach(chat => {
        const date = new Date(chat.created_at).toLocaleDateString()
        if (!groups[date]) {
          groups[date] = {
            date: date,
            chats: []
          }
        }
        groups[date].chats.push(chat)
      })
      return Object.values(groups).sort((a, b) => 
        new Date(b.date) - new Date(a.date)
      )
    })

    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const formatDateTime = (timestamp) => {
      return new Date(timestamp).toLocaleString([], {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const selectChat = (chat) => {
      selectedChat.value = chat
    }

    const loadChatHistory = async () => {
      isLoading.value = true
      error.value = ''
      noChats.value = false

      try {
        const data = await getDeviceChatHistory(deviceId)
        
        if (data.status === 'success') {
          // 检查是否有对话记录
          if (data.dialogue_count === 0 || !data.dialogue_list || data.dialogue_list.length === 0) {
            noChats.value = true
            chatHistory.value = []
            selectedChat.value = null
            return
          }
          
          // 转换对话列表为需要的格式
          chatHistory.value = data.dialogue_list.map((dialogue, index) => ({
            id: index + 1,
            session_id: dialogue.session_id,
            created_at: dialogue.create_time,
            title: dialogue.dialogue_title,
            messages: dialogue.message.filter(msg => msg.role !== 'system')
          }))

          // 设置选中的对话为第一个
          if (chatHistory.value.length > 0) {
            selectedChat.value = chatHistory.value[0]
          }
        } else if (data.status === 'not_found') {
          noChats.value = true
          chatHistory.value = []
          selectedChat.value = null
        } else {
          throw new Error('Failed to load chat history')
        }
      } catch (err) {
        error.value = '加载历史对话失败，请稍后重试'
        console.error('Error loading chat history:', err)
      } finally {
        isLoading.value = false
      }
    }

    const handleBack = () => {
      router.push('/console')
    }

    onMounted(() => {
      loadChatHistory()
    })

    return {
      deviceId,
      chatHistory,
      groupedChats,
      isLoading,
      error,
      noChats,
      searchText,
      selectedChat,
      handleBack,
      loadChatHistory,
      formatTime,
      formatDateTime,
      selectChat
    }
  }
}
</script>

<style scoped>
.chat-history-container {
  min-height: calc(100vh - 64px - 60px); /* 减去AppNav和AppFooter的高度 */
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
  position: fixed;
  top: 64px; /* AppNav的高度 */
  left: 0;
  right: 0;
  bottom: 60px; /* AppFooter的高度 */
}

.header {
  background: #fff;
  padding: 0.75rem 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  height: 48px;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  z-index: 10;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border: none;
  background: none;
  color: #666;
  cursor: pointer;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.back-btn:hover {
  color: #313a7e;
}

.arrow {
  font-size: 1.2rem;
}

.page-title {
  color: #333;
  font-size: 1.25rem;
  margin: 0;
}

.chat-layout {
  flex: 1;
  display: flex;
  overflow: hidden;
  margin: 0;
  background: #fff;
  box-shadow: none;
  border-radius: 0;
}

/* 左侧面板 */
.chat-list-panel {
  width: 280px;
  border-right: 1px solid #eee;
  display: flex;
  flex-direction: column;
  background: #fff;
  height: 100%;
}

.panel-header {
  padding: 0.75rem;
  border-bottom: 1px solid #eee;
  background: #fff;
}

.search-box input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #eee;
  border-radius: 4px;
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.2s;
}

.search-box input:focus {
  border-color: #313a7e;
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.75rem;
}

.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
  color: #666;
}

.error-message {
  text-align: center;
  padding: 1rem;
  color: #dc3545;
}

.retry-button {
  margin-top: 0.5rem;
  padding: 0.25rem 1rem;
  border: none;
  background: #313a7e;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.date-label {
  font-size: 0.8rem;
  color: #999;
  padding: 0.5rem 0;
  margin-top: 0.5rem;
}

.conversation-item {
  padding: 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-bottom: 0.5rem;
}

.conversation-item:hover {
  background-color: #f5f7fa;
}

.conversation-item.active {
  background-color: #e8f0fe;
}

.conversation-time {
  font-size: 0.8rem;
  color: #999;
  margin-bottom: 0.25rem;
}

.preview-message {
  font-size: 0.9rem;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  /* -webkit-line-clamp: 2; */
  -webkit-box-orient: vertical;
}

/* 右侧面板 */
.chat-content-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.panel-header {
  padding: 0.75rem;
  border-bottom: 1px solid #eee;
  background: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-time {
  color: #666;
  font-size: 0.9rem;
}

.session-id {
  color: #999;
  font-size: 0.9rem;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message-wrapper {
  display: flex;
  flex-direction: column;
}

.message {
  max-width: 70%;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  position: relative;
}

.user-message {
  align-self: flex-end;
  background: #313a7e;
  color: white;
  border-top-right-radius: 0;
}

.assistant-message {
  align-self: flex-start;
  background: white;
  color: #333;
  border-top-left-radius: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.message-content {
  font-size: 0.95rem;
  line-height: 1.5;
  white-space: pre-wrap;
}

.message-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.25rem;
  font-size: 0.75rem;
}

.ai-label {
  color: #666;
}

.message-time {
  font-size: 0.75rem;
  opacity: 0.8;
}

.empty-chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-chat p {
  font-size: 1rem;
  margin: 0;
}

.no-chats-message {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
  color: #999;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .chat-history-container {
    top: 64px;
  }

  .chat-layout {
    margin: 0;
  }

  .chat-list-panel {
    width: 240px;
  }

  .message {
    max-width: 85%;
  }
}

@media (max-width: 576px) {
  .chat-history-container {
    top: 64px;
    bottom: 60px;
  }

  .chat-layout {
    margin: 0;
    border-radius: 0;
  }

  .chat-list-panel {
    width: 100%;
    display: none;
  }

  .chat-list-panel.active {
    display: block;
  }

  .chat-content-panel {
    width: 100%;
  }

  .message {
    max-width: 90%;
  }
}
</style>