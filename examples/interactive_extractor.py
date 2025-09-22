"""
Interactive TED Transcript Extractor
交互式TED文字稿提取器
"""

import sys
import os
from pathlib import Path

# Add the parent directory to Python path to import ted_extractor
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ted_extractor import TEDTranscriptExtractor
from ted_extractor.utils import validate_ted_url, format_duration
import re


class InteractiveTEDExtractor:
    """交互式TED文字稿提取器"""
    
    def __init__(self):
        self.extractor = TEDTranscriptExtractor(delay_between_requests=1.0)
        self.extracted_talks = []
    
    def clean_filename(self, title):
        """清理标题作为文件名"""
        # 移除或替换不允许的字符
        cleaned = re.sub(r'[<>:"/\\|?*]', '', title)
        # 替换引号和其他特殊字符
        cleaned = cleaned.replace('"', '').replace("'", '')
        # 限制长度并去除首尾空格
        cleaned = cleaned.strip()[:100]  # 限制文件名长度
        return cleaned if cleaned else "untitled"
        
    def show_welcome(self):
        """显示欢迎信息"""
        print("=" * 70)
        print("        TED文字稿提取器 - 交互式模式")
        print("=" * 70)
        print("功能及使用方法:")
        print()
        print("  1. 提取单个TED演讲文字稿")
        print("     → 直接输入TED URL")
        print("     → 示例: https://www.ted.com/talks/speaker_name_talk_title")
        print()
        print("  2. 批量提取多个演讲")
        print("     → 输入命令: batch 或 批量")
        print("     → 然后逐行输入多个TED URL")
        print()
        print("  3. 查看提取历史")
        print("     → 输入命令: history 或 历史")
        print()
        print("  4. 保存结果到文件")
        print("     → 输入命令: save 或 保存")
        print("     → 支持JSON、CSV、TXT格式")
        print()
        print("  5. 其他命令")
        print("     → help 或 帮助 - 显示详细帮助")
        print("     → clear 或 清空 - 清空提取历史")
        print("     → quit 或 退出 - 退出程序")
        print()
        print("请输入命令或TED URL开始使用:")
        print("-" * 70)
    
    def show_help(self):
        """显示帮助信息"""
        print("\n" + "=" * 50)
        print("           详细帮助信息")
        print("=" * 50)
        print()
        print("【命令列表】")
        print("  help 或 帮助     - 显示此帮助信息")
        print("  history 或 历史  - 查看已提取的演讲列表")
        print("  save 或 保存     - 将提取结果保存到文件")
        print("  batch 或 批量    - 进入批量提取模式")
        print("  clear 或 清空    - 清空所有提取历史")
        print("  quit 或 退出     - 退出程序")
        print()
        print("【使用示例】")
        print("  单个提取:")
        print("    > https://www.ted.com/talks/brene_brown_the_power_of_vulnerability")
        print()
        print("  批量提取:")
        print("    > batch")
        print("    URL 1: https://www.ted.com/talks/talk1")
        print("    URL 2: https://www.ted.com/talks/talk2")
        print("    URL 3: (按回车结束)")
        print()
        print("  查看历史:")
        print("    > history")
        print()
        print("  保存结果:")
        print("    > save")
        print("    选择格式 (1-3): 1")
        print("    文件名: my_transcripts.json")
        print()
        print("【支持的URL格式】")
        print("  https://www.ted.com/talks/...")
        print("  https://ted.com/talks/...")
        print("-" * 50)
    
    def extract_single_interactive(self, url):
        """交互式提取单个演讲"""
        print(f"\n正在提取: {url}")
        print("请稍候...")
        
        talk = self.extractor.extract_single(url)
        
        if talk.success:
            self.extracted_talks.append(talk)
            
            print(f"\n[成功] 提取完成!")
            print(f"标题: {talk.title}")
            print(f"演讲者: {talk.speaker}")
            print(f"时长: {format_duration(talk.duration or 0)}")
            print(f"观看次数: {talk.views:,}" if talk.views else "观看次数: 未知")
            print(f"文字稿长度: {len(talk.transcript):,} 字符")
            print(f"单词数: {talk.get_word_count():,}")
            print(f"预计阅读时间: {talk.get_reading_time_minutes():.1f} 分钟")
            
            # 询问是否显示预览
            show_preview = input("\n是否显示文字稿预览? (y/n): ").lower().strip()
            if show_preview in ['y', 'yes', '是']:
                print(f"\n--- 文字稿预览 ---")
                preview_text = talk.transcript[:500] + "..." if len(talk.transcript) > 500 else talk.transcript
                print(preview_text)
            
            return True
        else:
            print(f"\n[失败] {talk.error_message}")
            return False
    
    def batch_extract_interactive(self):
        """交互式批量提取"""
        print("\n" + "=" * 50)
        print("           批量提取模式")
        print("=" * 50)
        print("请逐行输入TED演讲URL，每行一个")
        print("输入空行（直接按回车）完成输入")
        print()
        print("示例URL格式:")
        print("  https://www.ted.com/talks/speaker_name_talk_title")
        print("-" * 50)
        
        urls = []
        while True:
            url = input(f"URL {len(urls) + 1}: ").strip()
            
            if not url:  # 空行，结束输入
                break
                
            if validate_ted_url(url):
                urls.append(url)
                print(f"  已添加: {url}")
            else:
                print(f"  [警告] 无效的TED URL: {url}")
        
        if not urls:
            print("未输入有效的URL")
            return
        
        # 询问是否自动保存每个文件
        print(f"\n找到 {len(urls)} 个有效URL")
        auto_save = input("是否为每个演讲自动保存单独的文件? (y/n): ").lower().strip()
        save_format = None
        
        if auto_save in ['y', 'yes', '是']:
            print("\n选择保存格式:")
            print("  1. JSON - 包含完整数据")
            print("  2. CSV  - 表格格式")
            print("  3. TXT  - 仅文字稿内容")
            format_choice = input("选择格式 (1-3): ").strip()
            
            if format_choice == '1':
                save_format = 'json'
            elif format_choice == '2':
                save_format = 'csv'
            elif format_choice == '3':
                save_format = 'txt'
            else:
                print("无效选择，将不自动保存")
                save_format = None
        
        print(f"\n开始批量提取 {len(urls)} 个演讲...")
        
        def progress_callback(current, total, talk):
            status = "成功" if talk.success else "失败"
            print(f"[{current}/{total}] {status}: {talk.title or '未知标题'}")
            
            if not talk.success:
                print(f"  错误: {talk.error_message}")
            elif save_format and talk.success:
                # 自动保存单个文件
                try:
                    clean_title = self.clean_filename(talk.title)
                    filename = f"{clean_title}.{save_format}"
                    saved_file = self.extractor.save_results([talk], filename, save_format)
                    print(f"  已保存: {saved_file}")
                except Exception as e:
                    print(f"  保存失败: {e}")
        
        talks = self.extractor.extract_batch(urls, progress_callback)
        
        # 统计结果
        successful = [talk for talk in talks if talk.success]
        self.extracted_talks.extend(successful)
        
        print(f"\n批量提取完成:")
        print(f"  总数: {len(talks)}")
        print(f"  成功: {len(successful)}")
        print(f"  失败: {len(talks) - len(successful)}")
        
        if successful:
            total_words = sum(talk.get_word_count() for talk in successful)
            total_duration = sum(talk.duration or 0 for talk in successful)
            print(f"  总单词数: {total_words:,}")
            print(f"  总时长: {format_duration(total_duration)}")
            
            if save_format:
                print(f"\n已自动保存 {len(successful)} 个文件:")
                for talk in successful:
                    clean_title = self.clean_filename(talk.title)
                    filename = f"{clean_title}.{save_format}"
                    print(f"  - {filename}")
    
    def show_history(self):
        """显示提取历史"""
        if not self.extracted_talks:
            print("\n暂无提取历史")
            return
        
        print(f"\n=== 提取历史 ({len(self.extracted_talks)} 个演讲) ===")
        
        for i, talk in enumerate(self.extracted_talks, 1):
            print(f"\n{i}. {talk.title}")
            print(f"   演讲者: {talk.speaker}")
            print(f"   时长: {format_duration(talk.duration or 0)}")
            print(f"   单词数: {talk.get_word_count():,}")
            print(f"   提取时间: {talk.extracted_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def save_results_interactive(self):
        """交互式保存结果"""
        if not self.extracted_talks:
            print("\n暂无可保存的结果")
            return
        
        print(f"\n" + "=" * 50)
        print(f"      保存结果 ({len(self.extracted_talks)} 个演讲)")
        print("=" * 50)
        
        # 选择格式
        print("请选择保存格式:")
        print("  1. JSON - 包含完整数据（推荐，包含所有元数据）")
        print("  2. CSV  - 表格格式（适合Excel打开）")
        print("  3. TXT  - 纯文本格式（仅包含文字稿内容）")
        print()
        
        format_choice = input("选择格式 (1-3): ").strip()
        format_map = {'1': 'json', '2': 'csv', '3': 'txt'}
        
        if format_choice not in format_map:
            print("无效选择")
            return
        
        format_type = format_map[format_choice]
        
        # 如果有多个演讲，询问保存方式
        if len(self.extracted_talks) > 1:
            print(f"\n保存方式:")
            print("  1. 合并保存 - 所有演讲保存到一个文件")
            print("  2. 分开保存 - 每个演讲保存为单独文件（使用演讲标题作为文件名）")
            
            save_mode = input("选择保存方式 (1-2): ").strip()
            
            if save_mode == '2':
                # 分开保存每个演讲
                print(f"\n开始分开保存 {len(self.extracted_talks)} 个演讲...")
                saved_files = []
                
                for i, talk in enumerate(self.extracted_talks, 1):
                    try:
                        clean_title = self.clean_filename(talk.title)
                        filename = f"{clean_title}.{format_type}"
                        saved_file = self.extractor.save_results([talk], filename, format_type)
                        saved_files.append(saved_file)
                        print(f"[{i}/{len(self.extracted_talks)}] 已保存: {filename}")
                    except Exception as e:
                        print(f"[{i}/{len(self.extracted_talks)}] 保存失败: {talk.title} - {e}")
                
                print(f"\n[成功] 已分开保存 {len(saved_files)} 个文件:")
                for saved_file in saved_files:
                    file_path = Path(saved_file)
                    if file_path.exists():
                        file_size = file_path.stat().st_size
                        print(f"  - {file_path.name} ({file_size:,} 字节)")
                return
        
        # 合并保存（默认方式）
        default_filename = f"ted_transcripts.{format_type}"
        filename = input(f"文件名 (默认: {default_filename}): ").strip()
        
        if not filename:
            filename = default_filename
        
        # 保存文件
        try:
            saved_file = self.extractor.save_results(self.extracted_talks, filename, format_type)
            print(f"\n[成功] 结果已保存到: {saved_file}")
            
            # 显示文件信息
            file_path = Path(saved_file)
            if file_path.exists():
                file_size = file_path.stat().st_size
                print(f"文件大小: {file_size:,} 字节")
        
        except Exception as e:
            print(f"\n[失败] 保存失败: {e}")
    
    def clear_history(self):
        """清空提取历史"""
        if not self.extracted_talks:
            print("\n提取历史已为空")
            return
        
        confirm = input(f"\n确定要清空 {len(self.extracted_talks)} 个提取记录吗? (y/n): ").lower().strip()
        
        if confirm in ['y', 'yes', '是']:
            self.extracted_talks.clear()
            print("提取历史已清空")
        else:
            print("操作已取消")
    
    def run(self):
        """运行交互式提取器"""
        self.show_welcome()
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if not user_input:
                    continue
                
                # 处理命令
                if user_input.lower() in ['quit', 'exit', 'q', '退出']:
                    print("\n感谢使用TED文字稿提取器!")
                    break
                
                elif user_input.lower() in ['help', 'h', '帮助']:
                    self.show_help()
                
                elif user_input.lower() in ['history', '历史']:
                    self.show_history()
                
                elif user_input.lower() in ['save', '保存']:
                    self.save_results_interactive()
                
                elif user_input.lower() in ['batch', '批量']:
                    self.batch_extract_interactive()
                
                elif user_input.lower() in ['clear', '清空']:
                    self.clear_history()
                
                # 检查是否为TED URL
                elif user_input.startswith('http'):
                    if validate_ted_url(user_input):
                        self.extract_single_interactive(user_input)
                    else:
                        print("\n[错误] 请输入有效的TED演讲URL")
                        print("格式: https://www.ted.com/talks/...")
                
                else:
                    print(f"\n[错误] 未知命令: {user_input}")
                    print("输入 'help' 查看可用命令")
            
            except KeyboardInterrupt:
                print("\n\n程序被用户中断")
                break
            
            except Exception as e:
                print(f"\n[错误] 发生异常: {e}")


def main():
    """主函数"""
    try:
        extractor = InteractiveTEDExtractor()
        extractor.run()
    except Exception as e:
        print(f"程序启动失败: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
