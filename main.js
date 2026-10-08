const glados = async () => {
  const cookie = process.env.GLADOS
  if (!cookie) return
  try {
    const headers = {
      'cookie': cookie,
      'referer': 'https://glados.cloud/console/checkin',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36',
    }
    const checkin = await fetch('https://glados.cloud/api/user/checkin', {
      method: 'POST',
      headers: { ...headers, 'content-type': 'application/json' },
      body: '{"token":"glados.cloud"}',
    }).then((r) => r.json())
    const status = await fetch('https://glados.cloud/api/user/status', {
      method: 'GET',
      headers,
    }).then((r) => r.json())
    const leftDays = status?.data?.leftDays
    const automated = /automated/i.test(checkin?.message ?? '')
    if (automated || leftDays == null) {
      return [
        'Checkin Failed',
        `${checkin.message}`,
        `status: ${JSON.stringify(status).slice(0, 300)}`,
        'Cookie 可能已过期,请重新登录后更新 GitHub Secrets 的 GLADOS',
        `<${process.env.GITHUB_SERVER_URL}/${process.env.GITHUB_REPOSITORY}>`,
      ]
    }
    return [
      'Checkin OK',
      `${checkin.message}`,
      `Left Days ${Number(leftDays)}`,
    ]
  } catch (error) {
    return [
      'Checkin Error',
      `${error}`,
      `<${process.env.GITHUB_SERVER_URL}/${process.env.GITHUB_REPOSITORY}>`,
    ]
  }
}

const notify = async (contents) => {
  const token = process.env.NOTIFY
  if (!token || !contents) return
  await fetch(`https://www.pushplus.plus/send`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({
      token,
      title: contents[0],
      content: contents.join('<br>'),
      template: 'markdown',
    }),
  })
}

const main = async () => {
  const result = await glados()
  console.log(result);
  await notify(result)
}

main()
