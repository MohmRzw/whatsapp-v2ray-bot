const { default: makeWASocket, useSingleFileAuthState } = require('@whiskeysockets/baileys')
const P = require('pino')
const fs = require('fs')

const { state, saveState } = useSingleFileAuthState('./auth.json')

async function startBot() {
    const sock = makeWASocket({
        logger: P({ level: 'silent' }),
        printQRInTerminal: true,
        auth: state
    })

    sock.ev.on('creds.update', saveState)

    sock.ev.on('messages.upsert', async ({ messages }) => {
        const msg = messages[0]
        if (!msg.message || msg.key.fromMe) return

        const sender = msg.key.remoteJid
        const messageContent = msg.message.conversation || msg.message.imageMessage?.caption || ''

        console.log(`پیام از ${sender}: ${messageContent}`)

        if (messageContent === '1' || messageContent.includes('خرید')) {
            await sock.sendMessage(sender, {
                text: `💳 قیمت کانفیگ یک‌ماهه: 90,000 تومان

برای خرید لطفاً مبلغ را به شماره کارت زیر واریز کرده و عکس فیش را ارسال نمایید:

🏦 بانک ملت  
🔢 6104-3378-xxxx-xxxx  
📛 به نام: علی محمدی`
            })
        } else if (msg.message.imageMessage) {
            await sock.sendMessage(sender, {
                text: '📥 فیش شما دریافت شد. در حال بررسی است. لطفاً منتظر بمانید.'
            })
        } else {
            await sock.sendMessage(sender, {
                text: `👋 خوش اومدی به ربات فروش کانفیگ V2Ray!

لطفاً یکی از گزینه‌ها رو انتخاب کن:

1️⃣ خرید کانفیگ  
2️⃣ تمدید  
3️⃣ پشتیبانی`
            })
        }
    })
}

startBot()
