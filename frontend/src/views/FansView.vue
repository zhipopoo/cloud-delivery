<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useMemberStore } from '@/stores/members'
import { fansApi } from '@/api'
import type { FanMessage } from '@/types'
import { HeartOutlined, SendOutlined } from '@ant-design/icons-vue'

const memberStore = useMemberStore()
const messages = ref<Record<number, FanMessage[]>>({})
const newMessage = ref('')
const selectedMemberId = ref<number | null>(null)

onMounted(async () => {
  await memberStore.fetchMembers()
  for (const m of memberStore.members) {
    const res = await fansApi.getMessages(m.id)
    messages.value[m.id] = res.data
  }
})

async function sendMessage() {
  if (!selectedMemberId.value || !newMessage.value.trim()) return
  await fansApi.postMessage({
    member_id: selectedMemberId.value,
    author_name: 'Anonymous Colleague',
    content: newMessage.value.trim(),
  })
  const res = await fansApi.getMessages(selectedMemberId.value)
  messages.value[selectedMemberId.value] = res.data
  await memberStore.fetchMembers()
  newMessage.value = ''
}
</script>

<template>
  <div class="space-y-6">
    <!-- Fan Count Leaderboard -->
    <div class="geo-card p-5 animate-slide-up">
      <div class="mb-4 flex items-center gap-3">
        <HeartOutlined class="text-pink-400" />
        <h2 class="text-sm font-bold uppercase tracking-wider text-gray-900">Fan Leaderboard</h2>
      </div>

      <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="m in [...memberStore.members].sort((a, b) => b.fans_count - a.fans_count)"
          :key="m.id"
          class="geo-card-hover cursor-pointer p-4"
          :class="{ 'border-hw-blue/40': selectedMemberId === m.id }"
          @click="selectedMemberId = m.id"
        >
          <div class="flex items-center gap-3">
            <div class="avatar-hex h-12 w-12 flex-shrink-0 overflow-hidden bg-hw-red-50">
              <img :src="m.photo_url || `https://api.dicebear.com/7.x/bottts/svg?seed=${m.avatar_seed}`" class="h-full w-full" />
            </div>
            <div class="min-w-0 flex-1">
              <p class="text-sm font-bold text-gray-900">{{ m.name }}</p>
              <p class="text-xs text-hw-gray-600">{{ m.role }}</p>
            </div>
            <div class="flex flex-col items-center">
              <HeartOutlined class="text-pink-400" />
              <span class="text-lg font-bold glow-text">{{ m.fans_count }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Message Board -->
    <div v-if="selectedMemberId" class="geo-card p-5 animate-slide-up">
      <h2 class="mb-4 text-sm font-bold uppercase tracking-wider text-hw-red-500">
        Messages for {{ memberStore.members.find(m => m.id === selectedMemberId)?.name }}
      </h2>

      <div class="mb-4 max-h-64 space-y-2 overflow-y-auto pr-2">
        <div
          v-for="msg in (messages[selectedMemberId!] || [])"
          :key="msg.id"
          class="rounded-lg border border-hw-red-100 bg-hw-gray-100 p-3"
        >
          <div class="flex items-center justify-between">
            <span class="text-xs font-semibold text-hw-red-500">{{ msg.author_name }}</span>
            <span class="text-[10px] text-hw-gray-600">{{ new Date(msg.created_at).toLocaleDateString() }}</span>
          </div>
          <p class="mt-1 text-sm text-hw-gray-300">{{ msg.content }}</p>
        </div>
        <div v-if="!messages[selectedMemberId!]?.length" class="py-8 text-center text-xs text-hw-gray-600">
          No messages yet. Be the first fan!
        </div>
      </div>

      <!-- Input -->
      <div class="flex gap-2">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Write a message..."
          class="flex-1 rounded-lg border border-hw-red-200 bg-hw-gray-800 px-3 py-2 text-sm text-gray-900 placeholder-hw-gray-600 outline-none focus:border-gray-1000"
          @keyup.enter="sendMessage"
        />
        <button
          class="flex items-center gap-2 rounded-lg bg-hw-blue px-4 py-2 text-sm font-medium text-gray-900 transition-colors hover:bg-hw-blue-dark"
          @click="sendMessage"
        >
          <SendOutlined />
          Send
        </button>
      </div>
    </div>
  </div>
</template>