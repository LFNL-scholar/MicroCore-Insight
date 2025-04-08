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
                <div class="conversation-preview">
                  <div class="preview-message">{{ chat.user_message }}</div>
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
          </div>
          <div class="messages-container">
            <div class="message-wrapper">
              <div class="message user-message">
                <div class="message-content">{{ selectedChat.user_message }}</div>
                <div class="message-time">{{ formatTime(selectedChat.created_at) }}</div>
              </div>
            </div>
            <div class="message-wrapper">
              <div class="message assistant-message">
                <div class="message-content">{{ selectedChat.assistant_message }}</div>
                <div class="message-footer">
                  <span class="ai-label">AI生成</span>
                  <span class="message-time">{{ formatTime(selectedChat.created_at) }}</span>
                </div>
              </div>
            </div>
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

    // 按日期对聊天记录进行分组
    const groupedChats = computed(() => {
      const filtered = searchText.value
        ? chatHistory.value.filter(chat => 
            chat.user_message.toLowerCase().includes(searchText.value.toLowerCase()) ||
            chat.assistant_message.toLowerCase().includes(searchText.value.toLowerCase())
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

      try {
        // 模拟API调用延迟
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // 使用模拟数据
        chatHistory.value = [
          {
            id: 1,
            created_at: '2024-03-21 09:15:00',
            user_message: '你好，今天天气怎么样？',
            assistant_message: '根据当前位置的天气数据显示，今天是晴天，气温在20-25度之间，非常适合外出活动。建议可以适当增加户外运动时间，注意防晒。'
          },
          {
            id: 2,
            created_at: '2024-03-21 09:16:00',
            user_message: '那你给我推荐一些适合今天的户外活动吧',
            assistant_message: '考虑到今天的天气情况，我建议以下活动：\n1. 公园散步或慢跑\n2. 骑自行车郊游\n3. 野餐\n4. 户外摄影\n5. 打羽毛球\n\n这些活动都很适合现在的天气条件，既能享受阳光又不会太过剧烈。记得带足水和防晒用品！'
          },
          {
            id: 3,
            created_at: '2024-03-21 09:17:00',
            user_message: '好主意！那我打算去野餐，你能帮我规划一下需要准备什么吗？',
            assistant_message: '当然可以！以下是野餐必备清单：\n\n必需品：\n- 野餐垫\n- 便携餐具\n- 纸巾和湿巾\n- 垃圾袋\n- 防晒用品\n- 便携小风扇\n\n食物建议：\n- 三明治\n- 水果\n- 饮料\n- 小零食\n\n记得选择阴凉的地方，避免正午时分出行哦！'
          },
          {
            id: 4,
            created_at: '2024-03-21 14:30:00',
            user_message: '野餐很开心！现在我想了解一下附近有什么景点可以去看看',
            assistant_message: '很高兴你野餐愉快！让我为你推荐一些周边景点：\n\n1. 市中心公园 - 步行10分钟\n2. 艺术博物馆 - 驾车15分钟\n3. 滨江公园 - 步行20分钟\n4. 古城街区 - 驾车20分钟\n\n考虑到现在的时间，建议可以去滨江公园，那里傍晚的景色特别美！'
          }
          ,
          {
            id: 5,
            created_at: '2024-03-21 16:45:00',
            user_message: '我想了解一下中国古代四大发明的历史，你能详细介绍一下吗？',
            assistant_message: '我很乐意为您介绍中国古代四大发明！\n\n1. 造纸术：\n- 起源于西汉，由蔡伦改进完善于东汉\n- 取代了竹简和丝帛，大大降低了书写材料的成本\n- 对文化传播和知识记录产生了革命性影响\n\n2. 指南针：\n- 最早出现于战国时期，称为"司南"\n- 宋代发展出指南针，用于航海导航\n- 促进了世界航海事业的发展，推动了地理大发现\n\n3. 火药：\n- 始于唐代炼丹术的意外发现\n- 最初用于烟花爆竹，后发展为军事用途\n- 改变了世界军事发展历程\n\n4. 活字印刷：\n- 北宋毕昇发明泥活字印刷\n- 元代王祯改进为木活字\n- 大大提高了印刷效率，促进了文化传播\n\n这些发明对人类文明发展产生了深远影响，至今仍被认为是中国对世界文明最重要的贡献之一。每一项发明都经历了漫长的发展过程，并在不同时期发挥了重要作用。\n\n您对哪一项发明特别感兴趣？我可以为您提供更详细的信息。'
          }
        ]
      } catch (err) {
        error.value = '加载历史对话失败，请稍后重试'
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