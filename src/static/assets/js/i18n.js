/**
 * Système d'internationalisation (i18n) pour VCUY1
 * Gère la traduction FR/EN de toute l'application
 */

class I18n {
    constructor() {
        this.currentLang = localStorage.getItem('vcuy1_language') || 'fr';
        this.translations = {
            fr: {
                // Navigation
                'nav.home': 'Accueil',
                'nav.dashboard': 'Tableau de bord',
                'nav.volunteers': 'Volontaires',
                'nav.analytics': 'Analyses',
                'nav.about': 'À propos',
                
                // Hero Section
                'hero.title': 'Calcul Distribué',
                'hero.title.highlight': 'Volontaire',
                'hero.description': 'Exploitez la puissance collective des volontaires pour vos calculs intensifs. Économisez jusqu\'à',
                'hero.savings': 'd\'économies',
                'hero.cta.dashboard': 'Voir le Tableau de Bord',
                'hero.cta.learn': 'En Savoir Plus',
                
                // Stats
                'stats.volunteers': 'Volontaires Actifs',
                'stats.tasks': 'Tâches Traitées',
                'stats.savings': 'Économies Réalisées',
                'stats.cpu': 'Utilisation CPU',
                
                // Dashboard
                'dashboard.title': 'Tableau de Bord',
                'dashboard.subtitle': 'Vue d\'ensemble de votre système de calcul distribué',
                'dashboard.lastUpdate': 'Dernière mise à jour:',
                'dashboard.refresh': 'Actualiser',
                'dashboard.activeVolunteers': 'Volontaires Actifs',
                'dashboard.completedTasks': 'Tâches Complétées',
                'dashboard.cpuUsage': 'Utilisation CPU',
                'dashboard.costSavings': 'Économies',
                'dashboard.sinceYesterday': 'depuis hier',
                'dashboard.thisMonth': 'ce mois',
                'dashboard.performance': 'Performance Système',
                'dashboard.tasksDistribution': 'Distribution des Tâches',
                'dashboard.recentTasks': 'Tâches Récentes',
                
                // Volunteers
                'volunteers.title': 'Réseau de Volontaires',
                'volunteers.subtitle': 'Gérez et surveillez les performances de votre réseau de calcul distribué',
                'volunteers.total': 'Total Volontaires',
                'volunteers.active': 'Actifs',
                'volunteers.avgPerformance': 'Performance Moyenne',
                'volunteers.totalTime': 'Temps Total',
                'volunteers.search': 'Rechercher un volontaire...',
                'volunteers.allStatus': 'Tous les statuts',
                'volunteers.status.active': 'Actif',
                'volunteers.status.busy': 'Occupé',
                'volunteers.status.inactive': 'Inactif',
                'volunteers.details': 'Détails',
                'volunteers.showing': 'Affichage de',
                'volunteers.to': 'à',
                'volunteers.of': 'sur',
                'volunteers.previous': 'Précédent',
                'volunteers.next': 'Suivant',
                'volunteers.resources': 'Ressources',
                'volunteers.performance': 'Performance',
                'volunteers.tasks': 'Tâches',
                'volunteers.cores': 'cores',
                
                // Analytics
                'analytics.title': 'Analyses et Métriques',
                'analytics.subtitle': 'Analysez les performances et les économies de votre système',
                'analytics.costSavings': 'Économies de Coûts',
                'analytics.totalSavings': 'Économies Totales',
                'analytics.savings': 'd\'économies',
                'analytics.costPerTask': 'Coût par Tâche',
                'analytics.traditional': 'traditionnel',
                'analytics.tasksProcessed': 'Tâches Traitées',
                'analytics.viaVolunteers': 'via volontaires',
                'analytics.monthlyROI': 'ROI Mensuel',
                'analytics.return': 'Retour',
                'analytics.onInvestment': 'sur investissement',
                'analytics.performanceAnalytics': 'Analyses de Performance',
                'analytics.performanceHistory': 'Historique des Performances',
                'analytics.performanceDistribution': 'Distribution des Performances',
                'analytics.costComparison': 'Comparaison des Coûts',
                'analytics.topVolunteers': 'Top Volontaires',
                'analytics.globalStats': 'Statistiques Globales',
                'analytics.resourceUtilization': 'Utilisation des Ressources',
                'analytics.globalCPU': 'CPU Global',
                'analytics.globalMemory': 'Mémoire Globale',
                'analytics.network': 'Réseau',
                'analytics.avgUsage': 'Utilisation moyenne',
                'analytics.avgThroughput': 'Débit moyen',
                'analytics.last24h': 'Dernières 24h',
                'analytics.last7days': '7 derniers jours',
                'analytics.last30days': '30 derniers jours',
                
                // About
                'about.title': 'À Propos de VCUY1',
                'about.description': 'Un système révolutionnaire de calcul distribué volontaire développé à l\'Université de Yaoundé I',
                'about.mission': 'Notre Mission',
                'about.missionDesc': 'Rendre le calcul haute performance accessible à tous en exploitant la puissance collective des volontaires',
                'about.accessibility': 'Accessibilité',
                'about.accessibility.desc': 'Démocratiser l\'accès aux ressources de calcul pour les chercheurs, étudiants et entreprises',
                'about.sustainability': 'Durabilité',
                'about.sustainability.desc': 'Optimiser l\'utilisation des ressources existantes pour réduire l\'empreinte carbone',
                'about.collaboration': 'Collaboration',
                'about.collaboration.desc': 'Créer une communauté mondiale de contributeurs unis par la passion de la science',
                'about.technology': 'Architecture Technique',
                'about.technology.desc': 'VCUY1 est entièrement développé en Python pour garantir une intégration fluide',
                'about.server': 'Serveur Central',
                'about.server.desc': 'Architecture pub/sub avec Redis et MongoDB pour la gestion des workflows',
                'about.client': 'Application Client',
                'about.client.desc': 'Interface Python intuitive pour la soumission et le suivi des calculs',
                'about.docker': 'Conteneurisation Docker',
                'about.docker.desc': 'Isolation complète et sécurité maximale pour l\'exécution des tâches',
                'about.university': 'Université de Yaoundé I',
                'about.university.desc': 'VCUY1 est né de la recherche académique menée à l\'Université de Yaoundé I',
                'about.founded': 'Fondée en',
                'about.students': 'Étudiants',
                'about.benefits': 'Avantages du Système',
                'about.benefits.desc': 'VCUY1 offre des avantages significatifs par rapport aux solutions traditionnelles',
                'about.costReduction': 'Réduction des Coûts',
                'about.costReduction.desc': 'd\'économies par rapport aux solutions cloud traditionnelles',
                'about.security': 'Sécurité',
                'about.security.desc': 'isolation grâce à la conteneurisation Docker',
                'about.performance': 'Performance',
                'about.performance.desc': 'surveillance et optimisation en temps réel',
                'about.global': 'Global',
                'about.global.desc': 'réseau de volontaires dans le monde entier',
                'about.team': 'Équipe de Développement',
                'about.team.desc': 'Une équipe passionnée de chercheurs et d\'ingénieurs',
                'about.research': 'Équipe de Recherche',
                'about.research.desc': 'Chercheurs spécialisés en calcul distribué et systèmes parallèles',
                'about.developers': 'Développeurs',
                'about.developers.desc': 'Ingénieurs logiciels experts en Python, Docker et architectures distribuées',
                'about.community': 'Communauté',
                'about.community.desc': 'Réseau mondial de volontaires et contributeurs passionnés',
                'about.contact': 'Contact',
                'about.location': 'Localisation',
                'about.opensource': 'Open Source',
                'about.contribute': 'Contribuez sur GitHub',
                'about.joinUs': 'Rejoignez-nous',
                'about.joinUs.desc': 'Que vous soyez chercheur, développeur ou simplement passionné de technologie',
                'about.discover': 'Découvrir le Système',
                'about.becomeVolunteer': 'Devenir Volontaire',
                
                // Common
                'common.loading': 'Chargement...',
                'common.error': 'Erreur',
                'common.success': 'Succès',
                'common.close': 'Fermer',
                'common.cancel': 'Annuler',
                'common.confirm': 'Confirmer',
                'common.save': 'Enregistrer',
                'common.delete': 'Supprimer',
                'common.edit': 'Modifier',
                'common.view': 'Voir',
                'common.download': 'Télécharger',
                'common.upload': 'Téléverser',
                
                // Task Status
                'task.status.completed': 'Complétée',
                'task.status.running': 'En cours',
                'task.status.pending': 'En attente',
                'task.status.failed': 'Échouée',
                
                // Time
                'time.hours': 'heures',
                'time.minutes': 'minutes',
                'time.seconds': 'secondes',
                'time.days': 'jours',
                
                // Footer
                'footer.rights': 'Tous droits réservés',
                'footer.navigation': 'Navigation',
                'footer.resources': 'Ressources',
                'footer.documentation': 'Documentation',
                'footer.api': 'API',
                'footer.support': 'Support'
            },
            en: {
                // Navigation
                'nav.home': 'Home',
                'nav.dashboard': 'Dashboard',
                'nav.volunteers': 'Volunteers',
                'nav.analytics': 'Analytics',
                'nav.about': 'About',
                
                // Hero Section
                'hero.title': 'Volunteer Distributed',
                'hero.title.highlight': 'Computing',
                'hero.description': 'Leverage the collective power of volunteers for your intensive computations. Save up to',
                'hero.savings': 'in savings',
                'hero.cta.dashboard': 'View Dashboard',
                'hero.cta.learn': 'Learn More',
                
                // Stats
                'stats.volunteers': 'Active Volunteers',
                'stats.tasks': 'Tasks Processed',
                'stats.savings': 'Savings Achieved',
                'stats.cpu': 'CPU Usage',
                
                // Dashboard
                'dashboard.title': 'Dashboard',
                'dashboard.subtitle': 'Overview of your distributed computing system',
                'dashboard.lastUpdate': 'Last update:',
                'dashboard.refresh': 'Refresh',
                'dashboard.activeVolunteers': 'Active Volunteers',
                'dashboard.completedTasks': 'Completed Tasks',
                'dashboard.cpuUsage': 'CPU Usage',
                'dashboard.costSavings': 'Cost Savings',
                'dashboard.sinceYesterday': 'since yesterday',
                'dashboard.thisMonth': 'this month',
                'dashboard.performance': 'System Performance',
                'dashboard.tasksDistribution': 'Tasks Distribution',
                'dashboard.recentTasks': 'Recent Tasks',
                
                // Volunteers
                'volunteers.title': 'Volunteer Network',
                'volunteers.subtitle': 'Manage and monitor your distributed computing network performance',
                'volunteers.total': 'Total Volunteers',
                'volunteers.active': 'Active',
                'volunteers.avgPerformance': 'Average Performance',
                'volunteers.totalTime': 'Total Time',
                'volunteers.search': 'Search volunteer...',
                'volunteers.allStatus': 'All statuses',
                'volunteers.status.active': 'Active',
                'volunteers.status.busy': 'Busy',
                'volunteers.status.inactive': 'Inactive',
                'volunteers.details': 'Details',
                'volunteers.showing': 'Showing',
                'volunteers.to': 'to',
                'volunteers.of': 'of',
                'volunteers.previous': 'Previous',
                'volunteers.next': 'Next',
                'volunteers.resources': 'Resources',
                'volunteers.performance': 'Performance',
                'volunteers.tasks': 'Tasks',
                'volunteers.cores': 'cores',
                
                // Analytics
                'analytics.title': 'Analytics and Metrics',
                'analytics.subtitle': 'Analyze your system performance and savings',
                'analytics.costSavings': 'Cost Savings',
                'analytics.totalSavings': 'Total Savings',
                'analytics.savings': 'in savings',
                'analytics.costPerTask': 'Cost per Task',
                'analytics.traditional': 'traditional',
                'analytics.tasksProcessed': 'Tasks Processed',
                'analytics.viaVolunteers': 'via volunteers',
                'analytics.monthlyROI': 'Monthly ROI',
                'analytics.return': 'Return',
                'analytics.onInvestment': 'on investment',
                'analytics.performanceAnalytics': 'Performance Analytics',
                'analytics.performanceHistory': 'Performance History',
                'analytics.performanceDistribution': 'Performance Distribution',
                'analytics.costComparison': 'Cost Comparison',
                'analytics.topVolunteers': 'Top Volunteers',
                'analytics.globalStats': 'Global Statistics',
                'analytics.resourceUtilization': 'Resource Utilization',
                'analytics.globalCPU': 'Global CPU',
                'analytics.globalMemory': 'Global Memory',
                'analytics.network': 'Network',
                'analytics.avgUsage': 'Average usage',
                'analytics.avgThroughput': 'Average throughput',
                'analytics.last24h': 'Last 24h',
                'analytics.last7days': 'Last 7 days',
                'analytics.last30days': 'Last 30 days',
                
                // About
                'about.title': 'About VCUY1',
                'about.description': 'A revolutionary volunteer distributed computing system developed at the University of Yaoundé I',
                'about.mission': 'Our Mission',
                'about.missionDesc': 'Make high-performance computing accessible to all by leveraging the collective power of volunteers',
                'about.accessibility': 'Accessibility',
                'about.accessibility.desc': 'Democratize access to computing resources for researchers, students and businesses',
                'about.sustainability': 'Sustainability',
                'about.sustainability.desc': 'Optimize use of existing resources to reduce carbon footprint',
                'about.collaboration': 'Collaboration',
                'about.collaboration.desc': 'Create a global community of contributors united by passion for science',
                'about.technology': 'Technical Architecture',
                'about.technology.desc': 'VCUY1 is entirely developed in Python to ensure smooth integration',
                'about.server': 'Central Server',
                'about.server.desc': 'Pub/sub architecture with Redis and MongoDB for workflow management',
                'about.client': 'Client Application',
                'about.client.desc': 'Intuitive Python interface for computation submission and tracking',
                'about.docker': 'Docker Containerization',
                'about.docker.desc': 'Complete isolation and maximum security for task execution',
                'about.university': 'University of Yaoundé I',
                'about.university.desc': 'VCUY1 was born from academic research conducted at the University of Yaoundé I',
                'about.founded': 'Founded in',
                'about.students': 'Students',
                'about.benefits': 'System Benefits',
                'about.benefits.desc': 'VCUY1 offers significant advantages over traditional solutions',
                'about.costReduction': 'Cost Reduction',
                'about.costReduction.desc': 'savings compared to traditional cloud solutions',
                'about.security': 'Security',
                'about.security.desc': 'isolation through Docker containerization',
                'about.performance': 'Performance',
                'about.performance.desc': 'real-time monitoring and optimization',
                'about.global': 'Global',
                'about.global.desc': 'volunteer network worldwide',
                'about.team': 'Development Team',
                'about.team.desc': 'A passionate team of researchers and engineers',
                'about.research': 'Research Team',
                'about.research.desc': 'Researchers specialized in distributed computing and parallel systems',
                'about.developers': 'Developers',
                'about.developers.desc': 'Software engineers expert in Python, Docker and distributed architectures',
                'about.community': 'Community',
                'about.community.desc': 'Global network of passionate volunteers and contributors',
                'about.contact': 'Contact',
                'about.location': 'Location',
                'about.opensource': 'Open Source',
                'about.contribute': 'Contribute on GitHub',
                'about.joinUs': 'Join Us',
                'about.joinUs.desc': 'Whether you are a researcher, developer or simply passionate about technology',
                'about.discover': 'Discover the System',
                'about.becomeVolunteer': 'Become a Volunteer',
                
                // Common
                'common.loading': 'Loading...',
                'common.error': 'Error',
                'common.success': 'Success',
                'common.close': 'Close',
                'common.cancel': 'Cancel',
                'common.confirm': 'Confirm',
                'common.save': 'Save',
                'common.delete': 'Delete',
                'common.edit': 'Edit',
                'common.view': 'View',
                'common.download': 'Download',
                'common.upload': 'Upload',
                
                // Task Status
                'task.status.completed': 'Completed',
                'task.status.running': 'Running',
                'task.status.pending': 'Pending',
                'task.status.failed': 'Failed',
                
                // Time
                'time.hours': 'hours',
                'time.minutes': 'minutes',
                'time.seconds': 'seconds',
                'time.days': 'days',
                
                // Footer
                'footer.rights': 'All rights reserved',
                'footer.navigation': 'Navigation',
                'footer.resources': 'Resources',
                'footer.documentation': 'Documentation',
                'footer.api': 'API',
                'footer.support': 'Support'
            }
        };
    }
    
    /**
     * Obtenir la langue courante
     */
    getCurrentLanguage() {
        return this.currentLang;
    }
    
    /**
     * Changer la langue
     */
    setLanguage(lang) {
        if (this.translations[lang]) {
            this.currentLang = lang;
            localStorage.setItem('vcuy1_language', lang);
            this.translatePage();
            
            // Émettre un événement pour informer les autres composants
            window.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
        }
    }
    
    /**
     * Obtenir une traduction
     */
    t(key, params = {}) {
        const keys = key.split('.');
        let translation = this.translations[this.currentLang];
        
        for (const k of keys) {
            if (translation && translation[k]) {
                translation = translation[k];
            } else {
                return key; // Retourner la clé si traduction non trouvée
            }
        }
        
        // Remplacer les paramètres {param}
        if (typeof translation === 'string') {
            Object.keys(params).forEach(param => {
                translation = translation.replace(`{${param}}`, params[param]);
            });
        }
        
        return translation;
    }
    
    /**
     * Traduire toute la page
     */
    translatePage() {
        // Traduire tous les éléments avec data-i18n
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.t(key);
            
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.placeholder = translation;
            } else {
                element.textContent = translation;
            }
        });
        
        // Traduire les attributs title, alt, etc.
        document.querySelectorAll('[data-i18n-title]').forEach(element => {
            const key = element.getAttribute('data-i18n-title');
            element.title = this.t(key);
        });
        
        document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            element.placeholder = this.t(key);
        });
    }
    
    /**
     * Créer le sélecteur de langue
     */
    createLanguageSelector() {
        const selector = document.createElement('div');
        selector.className = 'language-selector';
        selector.innerHTML = `
            <button id="lang-fr" class="lang-btn ${this.currentLang === 'fr' ? 'active' : ''}" onclick="i18n.setLanguage('fr')">
                🇫🇷 FR
            </button>
            <button id="lang-en" class="lang-btn ${this.currentLang === 'en' ? 'active' : ''}" onclick="i18n.setLanguage('en')">
                🇬🇧 EN
            </button>
        `;
        
        return selector;
    }
    
    /**
     * Initialiser le système de traduction
     */
    init() {
        // Traduire la page au chargement
        this.translatePage();
        
        // Ajouter le sélecteur de langue à la navigation
        const nav = document.querySelector('nav .flex.items-center.space-x-8');
        if (nav) {
            const selector = this.createLanguageSelector();
            nav.appendChild(selector);
        }
        
        // Ajouter les styles CSS
        this.addStyles();
    }
    
    /**
     * Ajouter les styles pour le sélecteur de langue
     */
    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .language-selector {
                display: flex;
                gap: 0.5rem;
                align-items: center;
            }
            
            .lang-btn {
                padding: 0.5rem 1rem;
                border: 2px solid #e5e7eb;
                border-radius: 0.5rem;
                background: white;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 500;
                font-size: 0.875rem;
            }
            
            .lang-btn:hover {
                border-color: #2563eb;
                color: #2563eb;
                transform: translateY(-2px);
            }
            
            .lang-btn.active {
                background: #2563eb;
                color: white;
                border-color: #2563eb;
            }
            
            @media (max-width: 768px) {
                .language-selector {
                    position: fixed;
                    top: 1rem;
                    right: 1rem;
                    z-index: 100;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Créer une instance globale
const i18n = new I18n();

// Initialiser au chargement de la page
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => i18n.init());
} else {
    i18n.init();
}

// Exporter pour utilisation globale
window.i18n = i18n;