import React from 'react'
import { Button, Space, Tooltip } from 'antd'
import {
  SearchOutlined,
  FolderOpenOutlined,
  ReloadOutlined,
  DownloadOutlined,
  DeleteOutlined,
  EyeOutlined,
  EditOutlined,
  StarOutlined,
  StarFilled,
  ShareAltOutlined
} from '@ant-design/icons'

export interface ActionButton {
  key: string
  icon: React.ReactNode
  tooltip: string
  type?: 'primary' | 'default' | 'text' | 'link' | 'dashed'
  danger?: boolean
  onClick: () => void
  disabled?: boolean
}

interface ActionBarProps {
  actions: ActionButton[]
  maxVisible?: number
  size?: 'small' | 'middle' | 'large'
  className?: string
  style?: React.CSSProperties
}

const ActionBar: React.FC<ActionBarProps> = ({
  actions,
  maxVisible = 4,
  size = 'middle',
  className = '',
  style = {}
}) => {
  if (actions.length === 0) return null

  const visibleActions = actions.slice(0, maxVisible)
  const hiddenActions = actions.slice(maxVisible)

  return (
    <Space size="small" className={className} style={style}>
      {visibleActions.map((action) => (
        <Tooltip key={action.key} title={action.tooltip}>
          <Button
            type={action.type || 'text'}
            size={size}
            icon={action.icon}
            danger={action.danger}
            onClick={action.onClick}
            disabled={action.disabled}
          />
        </Tooltip>
      ))}

      {hiddenActions.length > 0 && (
        <Tooltip title={`更多操作 (${hiddenActions.length})`}>
          <Button type="text" size={size} icon={<EditOutlined />} />
        </Tooltip>
      )}
    </Space>
  )
}

// 预定义的常用操作按钮
export const FileActions = {
  Preview: (onClick: () => void, disabled = false): ActionButton => ({
    key: 'preview',
    icon: <EyeOutlined />,
    tooltip: '预览文件',
    onClick,
    disabled
  }),

  Open: (onClick: () => void, disabled = false): ActionButton => ({
    key: 'open',
    icon: <FolderOpenOutlined />,
    tooltip: '打开文件',
    onClick,
    disabled
  }),

  Download: (onClick: () => void, disabled = false): ActionButton => ({
    key: 'download',
    icon: <DownloadOutlined />,
    tooltip: '下载文件',
    onClick,
    disabled
  }),

  Delete: (onClick: () => void, disabled = false): ActionButton => ({
    key: 'delete',
    icon: <DeleteOutlined />,
    tooltip: '删除文件',
    onClick,
    disabled: false,
    danger: true
  }),

  Share: (onClick: () => void, disabled = false): ActionButton => ({
    key: 'share',
    icon: <ShareAltOutlined />,
    tooltip: '分享文件',
    onClick,
    disabled
  })
}

export const StarActions = {
  Add: (onClick: () => void, disabled = false): ActionButton => ({
    key: 'add-favorite',
    icon: <StarOutlined />,
    tooltip: '添加到收藏',
    onClick,
    disabled
  }),

  Remove: (onClick: () => void, disabled = false): ActionButton => ({
    key: 'remove-favorite',
    icon: <StarFilled />,
    tooltip: '取消收藏',
    onClick,
    disabled
  })
}

export const IndexActions = {
  Refresh: (onClick: () => void, disabled = false): ActionButton => ({
    key: 'refresh-index',
    icon: <ReloadOutlined />,
    tooltip: '刷新索引',
    onClick,
    disabled
  }),

  Scan: (onClick: () => void, disabled = false): ActionButton => ({
    key: 'scan-directory',
    icon: <SearchOutlined />,
    tooltip: '扫描目录',
    onClick,
    disabled
  })
}

export default ActionBar