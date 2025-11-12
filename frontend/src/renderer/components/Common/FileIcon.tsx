import React from 'react'
import {
  FileTextOutlined,
  FilePdfOutlined,
  FileWordOutlined,
  FileExcelOutlined,
  FilePptOutlined,
  FileMarkdownOutlined,
  FileImageOutlined,
  FileZipOutlined,
  FileUnknownOutlined,
  FolderOutlined,
  FolderOpenOutlined,
  VideoCameraOutlined,
  AudioOutlined,
  CodeOutlined,
  DatabaseOutlined
} from '@ant-design/icons'

export interface FileIconProps {
  fileType?: string
  fileName?: string
  isFolder?: boolean
  isOpen?: boolean
  size?: number
  style?: React.CSSProperties
  className?: string
}

const FileIcon: React.FC<FileIconProps> = ({
  fileType,
  fileName,
  isFolder = false,
  isOpen = false,
  size = 20,
  style = {},
  className = ''
}) => {
  if (isFolder) {
    const FolderIcon = isOpen ? FolderOpenOutlined : FolderOutlined
    return (
      <FolderIcon
        style={{
          fontSize: size,
          color: '#1890ff',
          ...style
        }}
        className={className}
      />
    )
  }

  // 从文件名提取扩展名
  const extension = fileType || (fileName ? fileName.split('.').pop()?.toLowerCase() : '')

  // 图标映射配置
  const iconMap: Record<string, {
    icon: React.ComponentType
    color: string
  }> = {
    // 文档类型
    'pdf': { icon: FilePdfOutlined, color: '#ff4d4f' },
    'doc': { icon: FileWordOutlined, color: '#1890ff' },
    'docx': { icon: FileWordOutlined, color: '#1890ff' },
    'xls': { icon: FileExcelOutlined, color: '#52c41a' },
    'xlsx': { icon: FileExcelOutlined, color: '#52c41a' },
    'ppt': { icon: FilePptOutlined, color: '#fa8c16' },
    'pptx': { icon: FilePptOutlined, color: '#fa8c16' },

    // 文本类型
    'txt': { icon: FileTextOutlined, color: '#722ed1' },
    'md': { icon: FileMarkdownOutlined, color: '#13c2c2' },
    'rtf': { icon: FileTextOutlined, color: '#722ed1' },

    // 图片类型
    'jpg': { icon: FileImageOutlined, color: '#fa541c' },
    'jpeg': { icon: FileImageOutlined, color: '#fa541c' },
    'png': { icon: FileImageOutlined, color: '#fa541c' },
    'gif': { icon: FileImageOutlined, color: '#fa541c' },
    'svg': { icon: FileImageOutlined, color: '#fa541c' },
    'bmp': { icon: FileImageOutlined, color: '#fa541c' },
    'webp': { icon: FileImageOutlined, color: '#fa541c' },

    // 压缩文件
    'zip': { icon: FileZipOutlined, color: '#8c8c8c' },
    'rar': { icon: FileZipOutlined, color: '#8c8c8c' },
    '7z': { icon: FileZipOutlined, color: '#8c8c8c' },
    'tar': { icon: FileZipOutlined, color: '#8c8c8c' },
    'gz': { icon: FileZipOutlined, color: '#8c8c8c' },

    // 音频文件
    'mp3': { icon: AudioOutlined, color: '#13c2c2' },
    'wav': { icon: AudioOutlined, color: '#13c2c2' },
    'flac': { icon: AudioOutlined, color: '#13c2c2' },
    'aac': { icon: AudioOutlined, color: '#13c2c2' },
    'ogg': { icon: AudioOutlined, color: '#13c2c2' },

    // 视频文件
    'mp4': { icon: VideoCameraOutlined, color: '#52c41a' },
    'avi': { icon: VideoCameraOutlined, color: '#52c41a' },
    'mkv': { icon: VideoCameraOutlined, color: '#52c41a' },
    'mov': { icon: VideoCameraOutlined, color: '#52c41a' },
    'wmv': { icon: VideoCameraOutlined, color: '#52c41a' },
    'flv': { icon: VideoCameraOutlined, color: '#52c41a' },
    'webm': { icon: VideoCameraOutlined, color: '#52c41a' },

    // 代码文件
    'js': { icon: CodeOutlined, color: '#fadb14' },
    'jsx': { icon: CodeOutlined, color: '#fadb14' },
    'ts': { icon: CodeOutlined, color: '#1890ff' },
    'tsx': { icon: CodeOutlined, color: '#1890ff' },
    'py': { icon: CodeOutlined, color: '#3776ab' },
    'java': { icon: CodeOutlined, color: '#f89820' },
    'cpp': { icon: CodeOutlined, color: '#00599c' },
    'c': { icon: CodeOutlined, color: '#a8b9cc' },
    'h': { icon: CodeOutlined, color: '#a8b9cc' },
    'css': { icon: CodeOutlined, color: '#1572b6' },
    'html': { icon: CodeOutlined, color: '#e34c26' },
    'xml': { icon: CodeOutlined, color: '#0060ac' },
    'json': { icon: CodeOutlined, color: '#000000' },
    'sql': { icon: DatabaseOutlined, color: '#336791' },
    'sh': { icon: CodeOutlined, color: '#89e051' },
    'bat': { icon: CodeOutlined, color: '#89e051' },
    'yml': { icon: CodeOutlined, color: '#cb171e' },
    'yaml': { icon: CodeOutlined, color: '#cb171e' },
    'ini': { icon: CodeOutlined, color: '#6d6d6d' }
  }

  const iconConfig = extension ? iconMap[extension] : null
  const IconComponent = iconConfig ? iconConfig.icon : FileUnknownOutlined
  const iconColor = iconConfig ? iconConfig.color : '#8c8c8c'

  return (
    <IconComponent
      style={{
        fontSize: size,
        color: iconColor,
        ...style
      }}
      className={className}
    />
  )
}

// 文件类型颜色映射
export const getFileTypeColor = (fileType: string): string => {
  const colorMap: Record<string, string> = {
    'pdf': '#ff4d4f',
    'doc': '#1890ff',
    'docx': '#1890ff',
    'xls': '#52c41a',
    'xlsx': '#52c41a',
    'ppt': '#fa8c16',
    'pptx': '#fa8c16',
    'txt': '#722ed1',
    'md': '#13c2c2',
    'jpg': '#fa541c',
    'png': '#fa541c',
    'zip': '#8c8c8c',
    'mp3': '#13c2c2',
    'mp4': '#52c41a',
    'js': '#fadb14',
    'py': '#3776ab'
  }

  return colorMap[fileType.toLowerCase()] || '#8c8c8c'
}

// 获取文件类型显示名称
export const getFileTypeLabel = (fileType: string): string => {
  const labelMap: Record<string, string> = {
    'pdf': 'PDF文档',
    'doc': 'Word文档',
    'docx': 'Word文档',
    'xls': 'Excel表格',
    'xlsx': 'Excel表格',
    'ppt': 'PowerPoint',
    'pptx': 'PowerPoint',
    'txt': '文本文件',
    'md': 'Markdown',
    'jpg': 'JPEG图片',
    'png': 'PNG图片',
    'svg': 'SVG图片',
    'zip': 'ZIP压缩包',
    'mp3': '音频文件',
    'mp4': '视频文件',
    'js': 'JavaScript',
    'ts': 'TypeScript',
    'py': 'Python'
  }

  return labelMap[fileType.toLowerCase()] || fileType.toUpperCase()
}

export default FileIcon