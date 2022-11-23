个人知识库管理链条中，使用Obsidian作为笔记管理软件，Pagenote(Chrome插件)作为离线文档阅读标注工具，使用SingleFile(Chrome插件)做离线网页剪切至知识库保存。
当修改了知识库保存文章的位置后，会导致该文章在Pagenote和Obsidian中的引用位置变化，从而Pagenote中看不见批注、Obsidian中的外链被破坏。
该项目会对Pagenote和Obsidian中的被破坏的连接进行修复。

注：目前支持pagenote版本为高于或等于0.24.0.2

当修改了知识库中文章的名称或位置后:

* 打开chrome浏览器，从pagenote中导出最新backup;
* 打开make_vault_index.py:
    * 确保指定知识库base路径正确，如果需要再指定索引文件路径（非必要）;
    * 运行即可;
    * 检查知识库生成的索引文件vault_index.txt，期间可以根据输出提示修复不合法的仓库知识库文件.
* 打开pagenote_relocation.py:
    * 确保知识库索引路径正确（即上一步生成的索引文件路径）;
    * 确保使用了pagenote最新导出的backup文件路径正确;
    * 运行即可.
    * 将生成的pagenote backup文件导入会pagenote插件
* 打开markdown_note_relocation.py:
    * 确保知识库索引路径正确（即第一步生成的索引文件路径）
    * 确保知识库的base_path配置正确（即Obsidian中的Vault地址）
    * 试运行可将参数do_write_disk=False，避免笔记直接被修改，检查无误后即可改为True
    * 若不想影响原笔记，则可将参数turn_on_backup=True，会生成一条新的带后缀"_modified"的笔记
    * 运行即可 
