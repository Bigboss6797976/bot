from aiogram import types
from keyboards.inline_menu import main_menu, back_button

async def handle_callbacks(callback_query: types.CallbackQuery):
    data = callback_query.data

    if data == "back_to_main":
        from handlers.start import cmd_start
        await cmd_start(callback_query.message)
        await callback_query.answer()
        return

    if data == "security":
        text = (
            "🔐 **J88宝博官方认证公告**\n\n"
            "唯一认证渠道：\n"
            "• 官方频道：@J88sportsbot\n"
            "• 官方群组：@J88sportsbot\n"
            "• 官方客服：@J88sportsbot\n"
            "• 游戏机器人：@J88sportsbot\n\n"
            "✅ 所有账号均带有官方认证标识\n"
            "✅ 充值提现全程保障\n"
            "✅ 官方直连，无中间风险"
        )
        await callback_query.message.edit_caption(
            caption=text,
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        await callback_query.answer()
        return

    if data == "risk":
        text = (
            "⚠️ **风险提示**\n\n"
            "任何未带官方认证标识的账号均非J88宝博官方渠道！\n"
            "请勿向非认证账户转账，谨防冒充客服诈骗。\n\n"
            "‼️ 声明：J88宝博国际娱乐只做海外市场，从不涉及中国市场。"
        )
        await callback_query.message.edit_caption(
            caption=text,
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        await callback_query.answer()
        return

    await callback_query.answer("请使用下方按钮操作")
