const CATEGORY_LABELS = {
  programming_languages: '编程语言',
  frameworks: '框架',
  databases: '数据库',
  cloud_services: '云服务',
  ai_tools: 'AI 工具',
  others: '其他',
}

export default function SkillTags({ skills }) {
  if (!skills) return null

  const allSkills = []
  for (const [category, items] of Object.entries(skills)) {
    if (Array.isArray(items) && items.length > 0) {
      const label = CATEGORY_LABELS[category] || category
      items.forEach((skill) => allSkills.push({ skill, category: label }))
    }
  }

  if (allSkills.length === 0) return null

  return (
    <div className="skill-tags-section">
      <h3>🛠 技能标签</h3>
      <div className="skill-tags">
        {allSkills.map(({ skill, category }, i) => (
          <span key={i} className="skill-tag" title={category}>
            {skill}
          </span>
        ))}
      </div>
    </div>
  )
}
