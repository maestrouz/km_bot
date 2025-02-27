<?php

define('TOKEN', '7799094741:AAHt16-4_mUypcrMbnU_MYDTrbksTSYrzHA');
define('FIRST_GROUP_LINK', 'https://t.me/Kimyo_markaz1');
define('MAIN_GROUP_LINK', 'https://t.me/Kimyo_markaz2');
define('DATA_FILE', 'users.json');

// Botni Telegram API-ga so'rov yuborish
function sendMessage($chat_id, $text) {
    $url = 'https://api.telegram.org/bot' . TOKEN . '/sendMessage?chat_id=' . $chat_id . '&text=' . urlencode($text);
    file_get_contents($url);
}

// Foydalanuvchi ma'lumotlarini yuklash
function loadData() {
    if (file_exists(DATA_FILE)) {
        return json_decode(file_get_contents(DATA_FILE), true);
    }
    return [];
}

// Foydalanuvchi ma'lumotlarini saqlash
function saveData($data) {
    file_put_contents(DATA_FILE, json_encode($data, JSON_PRETTY_PRINT));
}

function handleStartCommand($message) {
    $user_id = strval($message['from']['id']);
    $data = loadData();

    // Yangi foydalanuvchini saqlash
    if (!isset($data[$user_id])) {
        $data[$user_id] = ['referrals' => 0];
        saveData($data);
    }

    $referral_link = "https://t.me/YOUR_BOT_USERNAME?start={$user_id}"; // YOUR_BOT_USERNAME ni bot username bilan almashtiring
    $text = "Salom, {$message['from']['first_name']}! 👋\n\n" .
            "📢 Ushbu guruhga qo'shilish uchun siz 5 ta do‘stingizni taklif qilishingiz kerak!\n\n" .
            "📩 Sizning referal havolangiz:\n{$referral_link}\n\n" .
            "✅ Har bir yangi foydalanuvchi uchun 1 ball olasiz.\n" .
            "🎯 5 ball to‘plaganingizda, asosiy guruh havolasini olasiz!\n\n" .
            "🔗 Birinchi guruhga qo'shiling: " . FIRST_GROUP_LINK;

    sendMessage($message['chat']['id'], $text);
}

function handleReferral($message) {
    $args = explode(" ", $message['text']);
    if (count($args) > 1) {
        $referrer_id = $args[1];
        $user_id = strval($message['from']['id']);
        $data = loadData();

        // Yangi foydalanuvchini qo'shish va ballarni yangilash
        if ($user_id != $referrer_id && !isset($data[$user_id])) {
            $data[$user_id] = ['referrals' => 0];
            if (isset($data[$referrer_id])) {
                $data[$referrer_id]['referrals'] += 1;
                sendMessage($referrer_id, "🎉 Sizning do‘stingiz qo‘shildi! Sizda {$data[$referrer_id]['referrals']} ball bor!");

                // 5 ball to'planganda asosiy guruh havolasini yuborish
                if ($data[$referrer_id]['referrals'] >= 5) {
                    sendMessage($referrer_id, "🎊 Tabriklaymiz! Siz 5 ta do‘stingizni taklif qildingiz!\nAsosiy guruhga qo'shilish havolasi: " . MAIN_GROUP_LINK);
                }
            }

            saveData($data);
        }
    }
}

// Webhookni ishlatish
function handleWebhook() {
    $input = json_decode(file_get_contents('php://input'), true);
    $message = $input['message'];

    if (isset($message['text'])) {
        if (strpos($message['text'], '/start') === 0) {
            handleStartCommand($message);
            handleReferral($message);
        }
    }
}

// Webhookni chaqirish
handleWebhook();
?>
