/*
 * All text shown on the site lives here, so content edits never touch markup.
 * Facts come from docs/rag/*.md (the same source the RAG chatbot uses).
 *
 * Optional values set to null are hidden on the site until you fill them in.
 */

export const profile = {
  name: 'Arun Kumar P',
  initials: 'AK',
  role: 'Senior Software Engineer',
  company: 'Scalian Group India',
  email: 'test@skyleap.in',
  location: 'Bengaluru, Karnataka, India',
  locationShort: 'Bengaluru',
  timezone: 'IST (UTC+5:30)',
  status: 'Open to collaborations',
  snippet: 'print("Hello, World!")',
  heroIntro: {
    before: 'I build software from .NET and React applications to ',
    highlight1: 'computer vision models',
    middle: ' and, right now, ',
    highlight2: 'RAG and agentic AI',
    after: ' systems on AWS and Azure.',
  },
  aboutIntro:
    'I’m a Senior Software Engineer and team lead at Scalian Group India. Since 2022 I’ve delivered 10 to 20 projects across web development, machine learning, computer vision, generative AI and the cloud.',
  aboutSecondary:
    'I started as a trainee straight after my engineering degree in Electronics and Communication, was promoted within about six months, and today lead a small team of developers while staying hands-on.',
}

// Set a value to show the link; null hides it everywhere.
export const links = {
  linkedin: null,
  github: null,
  resumeUrl: null,
  portraitUrl: null,
}

export const focusAreas = ['.NET & React', 'Computer vision', 'RAG & agentic AI', 'Cloud (AWS, Azure)']

export const personalDetails = [
  { label: 'Full name', value: profile.name },
  { label: 'Role', value: `${profile.role} · ${profile.company}` },
  { label: 'Based in', value: `${profile.location} · ${profile.timezone}` },
  { label: 'Focus areas', value: focusAreas.join(' · ') },
  {
    label: 'Education',
    value: 'B.E., Electronics and Communication Engineering · Dayananda Sagar College of Engineering',
  },
  { label: 'Experience', value: 'Since 2022 · 10 to 20 projects across web, ML, computer vision and cloud' },
  { label: 'Languages', value: 'Kannada, English' },
  { label: 'Open to', value: 'Collaboration on AI, computer vision and RAG projects' },
]

export const skillGroups = [
  {
    title: 'Machine learning & AI',
    items: ['Python', 'PyTorch', 'PyTorch Lightning', 'MLflow', 'Computer vision', 'Deep learning'],
  },
  {
    title: 'LLMs & agents',
    items: ['RAG', 'Agentic AI', 'Vector databases', 'Embeddings'],
  },
  {
    title: 'Web & cloud',
    items: ['.NET', 'C#', 'React', 'AWS', 'AWS SageMaker', 'Azure'],
  },
]

export const experience = [
  {
    period: 'Present',
    role: 'Senior Software Engineer & Team Lead',
    company: 'Scalian Group India',
    summary: 'Leading a small team of developers: technical decisions, solution design, code reviews and mentoring.',
  },
  {
    period: '~6 months in',
    role: 'Software Engineer',
    company: 'Yucca IT Solutions (later acquired by Scalian Group India)',
    summary: 'Delivered projects across .NET, React, machine learning, computer vision and the cloud.',
  },
  {
    period: '2022',
    role: 'Trainee Software Engineer',
    company: 'Yucca IT Solutions',
    summary: 'Joined right after the engineering degree and contributed to real projects early on.',
  },
]

/*
 * visual: 'flow' (pipeline diagram) | 'grid' (attention grid) | 'layers' (app architecture)
 * caseStudyUrl: null hides the "Read case study" link.
 */
export const projects = [
  {
    id: 'portfolio-rag-chatbot',
    category: 'Generative AI',
    title: 'Portfolio RAG chatbot',
    summary:
      'A retrieval-augmented chatbot that answers questions about my background by chunking documents, embedding them with Amazon Titan and searching a Pinecone index.',
    tags: ['Python', 'AWS Bedrock', 'Pinecone', 'FastAPI'],
    visual: 'flow',
    flow: {
      top: ['question'],
      middle: ['embed · Titan', 'search · Pinecone', 'rank · chunks'],
      bottom: ['prompt + context', 'answer'],
    },
    caseStudyUrl: null,
  },
  {
    id: 'product-image-tagging',
    category: 'Computer vision',
    title: 'Product image tagging',
    summary:
      'A vision model, trained on AWS SageMaker, that looks at product photos and predicts tags such as category, type, colour and style, replacing slow manual labelling.',
    tags: ['AWS SageMaker', 'Computer vision', 'Deep learning'],
    visual: 'grid',
    caseStudyUrl: null,
  },
  {
    id: 'web-applications',
    category: 'Web & backend',
    title: '.NET and React applications',
    summary:
      'Web applications built and maintained on the Microsoft .NET platform with modern React front ends, deployed and run on AWS and Azure.',
    tags: ['C#', '.NET', 'React', 'Azure'],
    visual: 'layers',
    caseStudyUrl: null,
  },
]

// Empty lists hide their sections. Add entries to show them.
// research: [{ id, title, body, focus: [] }]
export const research = []
// writing: [{ id, category, date, title, summary, url }]
export const writing = []

export const contactTopics = ['RAG & agentic AI', 'Computer vision', '.NET & React']
