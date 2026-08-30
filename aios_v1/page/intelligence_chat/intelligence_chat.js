frappe.pages['intelligence-chat'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Department Intelligence',
        single_column: true
    });

    // Render HTML UI
    $(wrapper).find('.layout-main-section').html(`
        <div class="intelligence-chat-container">
            <!-- Header Info -->
            <div class="chat-header">
                <div class="header-status">
                    <span class="status-indicator"></span>
                    <span class="status-title">Department Intelligence Agent</span>
                    <span class="badge badge-primary">ERP AI Active</span>
                </div>
                <div class="header-desc">
                    Asisten analitis strategis perusahaan berbasis data aktual dan anti-halusinasi.
                </div>
            </div>

            <!-- Suggestion Chips -->
            <div class="suggestion-chips">
                <button class="chip-btn" data-query="Apa tugas utama Department Intelligence di perusahaan ini?">💡 Tugas Utama</button>
                <button class="chip-btn" data-query="Bagaimana status kesehatan performa bisnis saat ini?">📊 Analisis Performa</button>
                <button class="chip-btn" data-query="Apa saja risiko operasional yang perlu diwaspadai?">⚠️ Risiko & Rekomendasi</button>
            </div>

            <!-- Chat Messages Box -->
            <div class="chat-messages-box" id="chat-messages">
                <div class="chat-message assistant">
                    <div class="message-avatar">🤖</div>
                    <div class="message-bubble">
                        <div class="message-sender">Department Intelligence</div>
                        <div class="message-text">
                            Halo! Saya adalah <strong>Department Intelligence AI</strong>. Saya siap membantu menganalisis data, membaca dokumen laporan, dan memberikan rekomendasi strategis objektif untuk perusahaan Anda.
                            <br><br>
                            Ada yang ingin Anda analisis hari ini?
                        </div>
                    </div>
                </div>
            </div>

            <!-- Input Area -->
            <div class="chat-input-container">
                <textarea id="user-input" class="chat-textarea" placeholder="Ketik pertanyaan atau tugas analisis untuk AI... (Tekan Enter untuk kirim)" rows="2"></textarea>
                <button id="send-btn" class="chat-send-btn">
                    <span>Kirim</span> 🚀
                </button>
            </div>
        </div>
    `);

    const $messagesBox = $(wrapper).find('#chat-messages');
    const $userInput = $(wrapper).find('#user-input');
    const $sendBtn = $(wrapper).find('#send-btn');

    function scrollToBottom() {
        $messagesBox.scrollTop($messagesBox[0].scrollHeight);
    }

    function appendMessage(sender, text, isUser = false) {
        let formattedText = isUser ? frappe.utils.escape_html(text) : (frappe.markdown ? frappe.markdown(text) : text.replace(/\n/g, '<br>'));
        
        let avatar = isUser ? '👤' : '🤖';
        let msgClass = isUser ? 'user' : 'assistant';
        let senderLabel = isUser ? 'Anda' : 'Department Intelligence';

        let html = `
            <div class="chat-message ${msgClass}">
                <div class="message-avatar">${avatar}</div>
                <div class="message-bubble">
                    <div class="message-sender">${senderLabel}</div>
                    <div class="message-text">${formattedText}</div>
                </div>
            </div>
        `;
        $messagesBox.append(html);
        scrollToBottom();
    }

    function sendMessage() {
        let msg = $userInput.val().trim();
        if (!msg) return;

        appendMessage('User', msg, true);
        $userInput.val('');
        $userInput.prop('disabled', true);
        $sendBtn.prop('disabled', true).html('<span>Mikir...</span> ⏳');

        frappe.call({
            method: 'aios_v1.api.ask_intelligence',
            args: { message: msg },
            callback: function(r) {
                $userInput.prop('disabled', false);
                $sendBtn.prop('disabled', false).html('<span>Kirim</span> 🚀');
                $userInput.focus();

                if (r.message && r.message.success) {
                    appendMessage('Assistant', r.message.reply, false);
                } else {
                    let errMsg = (r.message && r.message.error) || 'Terjadi kesalahan sistem.';
                    appendMessage('Assistant', `⚠️ *Gagal mendapatkan respon:* ${errMsg}`, false);
                }
            },
            error: function(err) {
                $userInput.prop('disabled', false);
                $sendBtn.prop('disabled', false).html('<span>Kirim</span> 🚀');
                appendMessage('Assistant', `⚠️ *Error server:* ${err.statusText || 'Koneksi terputus.'}`, false);
            }
        });
    }

    $sendBtn.on('click', sendMessage);

    $userInput.on('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    $(wrapper).find('.chip-btn').on('click', function() {
        let query = $(this).data('query');
        $userInput.val(query);
        sendMessage();
    });
};
