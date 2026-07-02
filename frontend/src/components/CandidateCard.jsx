export default function CandidateCard({ basicInfo, jobIntention, education }) {
  if (!basicInfo) return null

  const items = [
    { label: '姓名', value: basicInfo.name },
    { label: '手机', value: basicInfo.phone },
    { label: '邮箱', value: basicInfo.email },
    { label: '地址', value: basicInfo.address },
  ]

  if (jobIntention) {
    items.push(
      { label: '求职意向', value: jobIntention.target_position },
      { label: '期望薪资', value: jobIntention.expected_salary },
      { label: '目标城市', value: jobIntention.target_city },
    )
  }

  if (education?.length > 0) {
    const edu = education[0]
    items.push({
      label: '学历',
      value: [edu.school, edu.degree, edu.major].filter(Boolean).join(' | '),
    })
  }

  return (
    <div className="candidate-card">
      <h3>👤 候选人信息</h3>
      <div className="info-grid">
        {items.map(
          (item) =>
            item.value && (
              <div key={item.label} className="info-item">
                <span className="info-label">{item.label}</span>
                <span className="info-value">{item.value}</span>
              </div>
            )
        )}
      </div>
    </div>
  )
}
