#!/usr/bin/env python3
"""
ARGUS - All-Seeing Eye
Social Media Reconnaissance Agent

Specializes in:
- Multi-platform social media monitoring
- Real-time feed analysis for missing persons
- Content pattern recognition
- Automated screenshot and evidence collection
"""

import asyncio
import json
import re
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass

import aiohttp
import tweepy
import instaloader
import praw
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..core.agent_base import ObsidianAgent, Priority
from ..core.ai_service_manager import QueryType, QueryContext, AGENT_PROMPTS

@dataclass
class SocialMediaProfile:
    """Social media profile information"""
    platform: str
    username: str
    display_name: str
    bio: str
    location: str
    follower_count: int
    following_count: int
    post_count: int
    profile_image_url: str
    verified: bool
    created_date: Optional[datetime]
    last_activity: Optional[datetime]
    posts: List[Dict]
    connections: List[str]
    metadata: Dict[str, Any]

@dataclass
class SocialMediaPost:
    """Individual social media post"""
    platform: str
    post_id: str
    username: str
    content: str
    timestamp: datetime
    engagement: Dict[str, int]  # likes, shares, comments
    location: Optional[str]
    media_urls: List[str]
    hashtags: List[str]
    mentions: List[str]
    metadata: Dict[str, Any]

class ARGUSAgent(ObsidianAgent):
    """
    ARGUS - All-Seeing Eye Social Media Reconnaissance Agent
    
    Monitors social media platforms for traces of missing persons,
    trafficking indicators, and suspicious activity patterns.
    """
    
    def __init__(self):
        super().__init__(
            name="ARGUS - All-Seeing Eye",
            codename="ARGUS",
            specialization="Social Media Reconnaissance",
            tools=[
                "tweepy", "instaloader", "facebook-scraper", "tiktok-scraper",
                "selenium", "scrapy", "social-analyzer", "sherlock",
                "linkedin-api", "reddit-praw", "discord-py", "telegram-scraper"
            ],
            ai_backends=["claude", "chatgpt", "local"]
        )
        
        # Platform clients
        self.twitter_client = None
        self.instagram_client = None
        self.reddit_client = None
        self.selenium_driver = None
        
        # Monitoring configuration
        self.monitored_keywords: Set[str] = set()
        self.monitored_users: Set[str] = set()
        self.monitored_locations: Set[str] = set()
        
        # Content analysis patterns
        self.trafficking_indicators = [
            r'\b(?:escort|massage)\b',
            r'\bmeet\s+now\b',
            r'\bdiscrete|discreet\b',
            r'\bcash\s+only\b',
            r'\bno\s+questions\s+asked\b',
            r'\byoung\s+(?:girl|woman)\b',
            r'\bnew\s+in\s+town\b'
        ]
        
        self.distress_patterns = [
            r'\bhelp\s+me\b',
            r'\bcan\'t\s+leave\b',
            r'\btrapped\b',
            r'\bscared\b',
            r'\bneed\s+(?:help|rescue)\b'
        ]
        
        # Evidence collection
        self.screenshot_dir = "/tmp/argus-screenshots"
        
    async def initialize_platforms(self, config: Dict[str, str]):
        """Initialize social media platform clients"""
        self.logger.info("Initializing social media platform clients...")
        
        # Twitter/X
        if config.get("twitter_bearer_token"):
            self.twitter_client = tweepy.Client(
                bearer_token=config["twitter_bearer_token"],
                consumer_key=config.get("twitter_api_key"),
                consumer_secret=config.get("twitter_api_secret"),
                access_token=config.get("twitter_access_token"),
                access_token_secret=config.get("twitter_access_secret"),
                wait_on_rate_limit=True
            )
        
        # Instagram
        self.instagram_client = instaloader.Instaloader()
        
        # Reddit
        if config.get("reddit_client_id"):
            self.reddit_client = praw.Reddit(
                client_id=config["reddit_client_id"],
                client_secret=config["reddit_client_secret"],
                user_agent="ARGUS-Social-Monitor/1.0"
            )
        
        # Selenium for dynamic content
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.selenium_driver = webdriver.Chrome(options=chrome_options)
        
        self.logger.info("Social media platform clients initialized")
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Return ARGUS capabilities"""
        return {
            "supported_tasks": [
                "social_media_search",
                "profile_analysis", 
                "content_monitoring",
                "user_tracking",
                "content_analysis",
                "evidence_collection",
                "pattern_recognition",
                "real_time_monitoring"
            ],
            "platforms": [
                "twitter", "instagram", "facebook", "tiktok", 
                "linkedin", "reddit", "discord", "telegram",
                "snapchat", "youtube", "pinterest"
            ],
            "analysis_types": [
                "missing_person_traces",
                "trafficking_indicators", 
                "suspicious_activity",
                "relationship_mapping",
                "content_verification",
                "location_analysis",
                "temporal_patterns"
            ]
        }
    
    async def analyze(self, data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Core analysis method for social media intelligence"""
        analysis_type = data.get("type", "general_analysis")
        
        self.logger.info(f"Starting {analysis_type} analysis")
        
        if analysis_type == "social_media_search":
            return await self._analyze_social_media_search(data, context)
        elif analysis_type == "profile_analysis":
            return await self._analyze_profile(data, context)
        elif analysis_type == "content_monitoring":
            return await self._analyze_content_monitoring(data, context)
        elif analysis_type == "user_tracking":
            return await self._analyze_user_tracking(data, context)
        elif analysis_type == "pattern_recognition":
            return await self._analyze_patterns(data, context)
        else:
            return await self._general_analysis(data, context)
    
    async def _analyze_social_media_search(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive social media search for a person"""
        subject_info = data.get("subject", {})
        search_terms = self._generate_search_terms(subject_info)
        
        results = {
            "subject": subject_info,
            "search_terms": search_terms,
            "platforms": {},
            "potential_matches": [],
            "trafficking_indicators": [],
            "urgent_findings": [],
            "confidence_score": 0.0,
            "timestamp": datetime.now().isoformat()
        }
        
        # Search across platforms
        platforms_to_search = data.get("platforms", ["twitter", "instagram", "facebook", "reddit"])
        
        for platform in platforms_to_search:
            try:
                platform_results = await self._search_platform(platform, search_terms)
                results["platforms"][platform] = platform_results
                
                # Analyze results for matches and indicators
                matches = await self._analyze_potential_matches(platform_results, subject_info)
                results["potential_matches"].extend(matches)
                
                # Check for trafficking indicators
                indicators = await self._check_trafficking_indicators(platform_results)
                results["trafficking_indicators"].extend(indicators)
                
            except Exception as e:
                self.logger.error(f"Error searching {platform}: {e}")
                results["platforms"][platform] = {"error": str(e)}
        
        # AI-powered analysis of findings
        ai_analysis = await self._ai_analyze_findings(results, context)
        results.update(ai_analysis)
        
        # Generate confidence score
        results["confidence_score"] = self._calculate_confidence_score(results)
        
        return results
    
    def _generate_search_terms(self, subject_info: Dict[str, Any]) -> List[str]:
        """Generate comprehensive search terms for a subject"""
        terms = []
        
        # Name variations
        if "name" in subject_info:
            name = subject_info["name"]
            terms.append(name)
            
            # Add name parts
            name_parts = name.split()
            if len(name_parts) > 1:
                terms.extend(name_parts)
                
                # First + Last combinations
                if len(name_parts) >= 2:
                    terms.append(f"{name_parts[0]} {name_parts[-1]}")
        
        # Aliases
        if "aliases" in subject_info:
            terms.extend(subject_info["aliases"])
        
        # Username patterns
        if "usernames" in subject_info:
            terms.extend(subject_info["usernames"])
        
        # Email addresses (username parts)
        if "emails" in subject_info:
            for email in subject_info["emails"]:
                username = email.split("@")[0]
                terms.append(username)
        
        # Phone numbers
        if "phone_numbers" in subject_info:
            terms.extend(subject_info["phone_numbers"])
        
        # Location-based terms
        if "locations" in subject_info:
            for location in subject_info["locations"]:
                terms.append(f'"{subject_info.get("name", "")}" "{location}"')
        
        return list(set(terms))  # Remove duplicates
    
    async def _search_platform(self, platform: str, search_terms: List[str]) -> Dict[str, Any]:
        """Search specific platform for terms"""
        if platform == "twitter" and self.twitter_client:
            return await self._search_twitter(search_terms)
        elif platform == "instagram":
            return await self._search_instagram(search_terms)
        elif platform == "reddit" and self.reddit_client:
            return await self._search_reddit(search_terms)
        elif platform == "facebook":
            return await self._search_facebook(search_terms)
        else:
            return {"error": f"Platform {platform} not supported or not configured"}
    
    async def _search_twitter(self, search_terms: List[str]) -> Dict[str, Any]:
        """Search Twitter/X for terms"""
        results = {"posts": [], "users": [], "metadata": {}}
        
        try:
            for term in search_terms[:5]:  # Limit to avoid rate limits
                # Search tweets
                tweets = self.twitter_client.search_recent_tweets(
                    query=f'"{term}"',
                    max_results=50,
                    tweet_fields=['created_at', 'author_id', 'geo', 'attachments', 'public_metrics']
                )
                
                if tweets.data:
                    for tweet in tweets.data:
                        post = SocialMediaPost(
                            platform="twitter",
                            post_id=tweet.id,
                            username=str(tweet.author_id),
                            content=tweet.text,
                            timestamp=tweet.created_at,
                            engagement={
                                "likes": tweet.public_metrics.get("like_count", 0),
                                "retweets": tweet.public_metrics.get("retweet_count", 0),
                                "replies": tweet.public_metrics.get("reply_count", 0)
                            },
                            location=tweet.geo.get("coordinates") if tweet.geo else None,
                            media_urls=[],
                            hashtags=re.findall(r'#\w+', tweet.text),
                            mentions=re.findall(r'@\w+', tweet.text),
                            metadata={"search_term": term}
                        )
                        results["posts"].append(post.__dict__)
                
                # Search users
                users = self.twitter_client.search_users(query=term, max_results=10)
                if users.data:
                    for user in users.data:
                        user_profile = {
                            "platform": "twitter",
                            "username": user.username,
                            "display_name": user.name,
                            "bio": user.description or "",
                            "location": user.location or "",
                            "follower_count": user.public_metrics.get("followers_count", 0),
                            "following_count": user.public_metrics.get("following_count", 0),
                            "verified": user.verified,
                            "created_date": user.created_at,
                            "search_term": term
                        }
                        results["users"].append(user_profile)
                
                await asyncio.sleep(1)  # Rate limiting
                
        except Exception as e:
            self.logger.error(f"Twitter search error: {e}")
            results["error"] = str(e)
        
        return results
    
    async def _search_instagram(self, search_terms: List[str]) -> Dict[str, Any]:
        """Search Instagram for terms"""
        results = {"posts": [], "users": [], "metadata": {}}
        
        try:
            for term in search_terms[:3]:  # Instagram is more rate-limited
                # Search hashtags
                try:
                    hashtag = instaloader.Hashtag.from_name(self.instagram_client.context, term.replace(" ", ""))
                    posts = hashtag.get_posts()
                    
                    count = 0
                    for post in posts:
                        if count >= 20:  # Limit posts per hashtag
                            break
                        
                        ig_post = {
                            "platform": "instagram",
                            "post_id": post.shortcode,
                            "username": post.owner_username,
                            "content": post.caption or "",
                            "timestamp": post.date,
                            "engagement": {
                                "likes": post.likes,
                                "comments": post.comments
                            },
                            "location": post.location.name if post.location else None,
                            "media_urls": [post.url],
                            "hashtags": post.caption_hashtags,
                            "mentions": post.caption_mentions,
                            "metadata": {"search_term": term}
                        }
                        results["posts"].append(ig_post)
                        count += 1
                        
                except Exception as e:
                    self.logger.warning(f"Instagram hashtag search failed for {term}: {e}")
                
                await asyncio.sleep(2)  # Rate limiting
                
        except Exception as e:
            self.logger.error(f"Instagram search error: {e}")
            results["error"] = str(e)
        
        return results
    
    async def _search_reddit(self, search_terms: List[str]) -> Dict[str, Any]:
        """Search Reddit for terms"""
        results = {"posts": [], "users": [], "metadata": {}}
        
        try:
            for term in search_terms[:5]:
                # Search submissions
                for submission in self.reddit_client.subreddit("all").search(term, limit=20):
                    reddit_post = {
                        "platform": "reddit",
                        "post_id": submission.id,
                        "username": str(submission.author) if submission.author else "[deleted]",
                        "content": f"{submission.title}\n{submission.selftext}",
                        "timestamp": datetime.fromtimestamp(submission.created_utc),
                        "engagement": {
                            "upvotes": submission.score,
                            "comments": submission.num_comments
                        },
                        "location": None,
                        "media_urls": [submission.url] if submission.url else [],
                        "hashtags": [],
                        "mentions": [],
                        "metadata": {
                            "subreddit": str(submission.subreddit),
                            "search_term": term
                        }
                    }
                    results["posts"].append(reddit_post)
                
                await asyncio.sleep(1)
                
        except Exception as e:
            self.logger.error(f"Reddit search error: {e}")
            results["error"] = str(e)
        
        return results
    
    async def _search_facebook(self, search_terms: List[str]) -> Dict[str, Any]:
        """Search Facebook using Selenium (limited due to restrictions)"""
        results = {"posts": [], "users": [], "metadata": {"note": "Facebook search limited due to platform restrictions"}}
        
        # Facebook has severe restrictions on automated searching
        # This would require special permissions and careful implementation
        # For now, return placeholder with note about limitations
        
        return results
    
    async def _analyze_potential_matches(self, platform_results: Dict[str, Any], subject_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze platform results for potential matches"""
        matches = []
        
        subject_name = subject_info.get("name", "").lower()
        subject_usernames = [u.lower() for u in subject_info.get("usernames", [])]
        subject_aliases = [a.lower() for a in subject_info.get("aliases", [])]
        
        # Check user profiles
        for user in platform_results.get("users", []):
            match_score = 0
            match_reasons = []
            
            username = user.get("username", "").lower()
            display_name = user.get("display_name", "").lower()
            bio = user.get("bio", "").lower()
            
            # Name matching
            if subject_name in display_name or display_name in subject_name:
                match_score += 50
                match_reasons.append("Name match in display name")
            
            # Username matching  
            for subject_username in subject_usernames:
                if subject_username in username:
                    match_score += 40
                    match_reasons.append(f"Username similarity: {subject_username}")
            
            # Alias matching
            for alias in subject_aliases:
                if alias in display_name or alias in bio:
                    match_score += 30
                    match_reasons.append(f"Alias match: {alias}")
            
            # Location matching
            user_location = user.get("location", "").lower()
            if user_location:
                for subject_location in subject_info.get("locations", []):
                    if subject_location.lower() in user_location:
                        match_score += 20
                        match_reasons.append(f"Location match: {subject_location}")
            
            if match_score >= 30:  # Threshold for potential match
                matches.append({
                    "type": "profile_match",
                    "platform": user.get("platform"),
                    "profile": user,
                    "match_score": match_score,
                    "match_reasons": match_reasons,
                    "confidence": min(match_score / 100, 1.0)
                })
        
        return matches
    
    async def _check_trafficking_indicators(self, platform_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for human trafficking indicators in content"""
        indicators = []
        
        for post in platform_results.get("posts", []):
            content = post.get("content", "").lower()
            
            # Check trafficking patterns
            for pattern in self.trafficking_indicators:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    indicators.append({
                        "type": "trafficking_indicator",
                        "pattern": pattern,
                        "matches": matches,
                        "post": post,
                        "severity": "HIGH",
                        "requires_immediate_attention": True
                    })
            
            # Check distress patterns
            for pattern in self.distress_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    indicators.append({
                        "type": "distress_indicator", 
                        "pattern": pattern,
                        "matches": matches,
                        "post": post,
                        "severity": "CRITICAL",
                        "requires_immediate_attention": True
                    })
        
        return indicators
    
    async def _ai_analyze_findings(self, results: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to analyze findings and provide insights"""
        from ..core.ai_service_manager import AIServiceManager
        
        # Prepare data for AI analysis
        analysis_prompt = f"""
        Analyze these social media search results for a missing person investigation:
        
        Subject: {results['subject']}
        Platforms Searched: {list(results['platforms'].keys())}
        Potential Matches: {len(results['potential_matches'])}
        Trafficking Indicators: {len(results['trafficking_indicators'])}
        
        Key Findings:
        {json.dumps(results['potential_matches'], indent=2)}
        
        Please provide:
        1. Assessment of match likelihood for each potential profile
        2. Priority ranking of leads to investigate
        3. Red flags or concerning patterns identified
        4. Recommended immediate actions
        5. Timeline analysis if temporal patterns are visible
        """
        
        try:
            ai_manager = AIServiceManager()  # Would be injected in real implementation
            query_context = QueryContext(
                agent_name="ARGUS",
                case_id=context.get("case_id", "unknown"),
                priority=Priority.HIGH.value,
                query_type=QueryType.INVESTIGATION,
                specialization="social_media_analysis"
            )
            
            ai_response = await ai_manager.route_query(
                analysis_prompt,
                query_context,
                AGENT_PROMPTS["ARGUS"]
            )
            
            return {
                "ai_analysis": ai_response.content,
                "ai_confidence": ai_response.confidence,
                "analysis_provider": ai_response.provider.value,
                "analysis_timestamp": ai_response.timestamp.isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"AI analysis error: {e}")
            return {
                "ai_analysis": f"AI analysis failed: {e}",
                "ai_confidence": 0.0
            }
    
    def _calculate_confidence_score(self, results: Dict[str, Any]) -> float:
        """Calculate overall confidence score for findings"""
        total_score = 0.0
        factors = 0
        
        # Platform coverage
        platform_coverage = len([p for p in results["platforms"].values() if "error" not in p])
        total_score += min(platform_coverage * 0.2, 0.4)  # Max 0.4 for platform coverage
        factors += 1
        
        # Match quality
        if results["potential_matches"]:
            avg_match_score = sum(m.get("match_score", 0) for m in results["potential_matches"]) / len(results["potential_matches"])
            total_score += min(avg_match_score / 100, 0.6)  # Max 0.6 for match quality
            factors += 1
        
        # Urgency indicators
        if results["trafficking_indicators"]:
            total_score += 0.3  # Boost for trafficking indicators
            factors += 1
        
        return total_score / max(factors, 1)
    
    async def start_monitoring(self, subjects: List[Dict[str, Any]], keywords: List[str]):
        """Start real-time monitoring for subjects and keywords"""
        self.logger.info(f"Starting monitoring for {len(subjects)} subjects and {len(keywords)} keywords")
        
        # Add to monitoring sets
        for subject in subjects:
            if "name" in subject:
                self.monitored_keywords.add(subject["name"])
            for alias in subject.get("aliases", []):
                self.monitored_keywords.add(alias)
        
        self.monitored_keywords.update(keywords)
        
        # Start monitoring tasks
        asyncio.create_task(self._monitor_twitter_stream())
        asyncio.create_task(self._monitor_instagram_hashtags())
        asyncio.create_task(self._monitor_reddit_mentions())
    
    async def _monitor_twitter_stream(self):
        """Monitor Twitter real-time stream"""
        # Implementation would use Twitter streaming API
        # This is a placeholder for the streaming logic
        pass
    
    async def _monitor_instagram_hashtags(self):
        """Monitor Instagram hashtags"""
        # Implementation would periodically check hashtags
        pass
    
    async def _monitor_reddit_mentions(self):
        """Monitor Reddit for keyword mentions"""
        # Implementation would use Reddit's API for mention tracking
        pass
    
    async def take_evidence_screenshot(self, url: str, case_id: str) -> str:
        """Take screenshot of social media content for evidence"""
        try:
            self.selenium_driver.get(url)
            await asyncio.sleep(3)  # Wait for page load
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            filename = f"{case_id}_{timestamp}_{url_hash}.png"
            filepath = f"{self.screenshot_dir}/{filename}"
            
            # Take screenshot
            self.selenium_driver.save_screenshot(filepath)
            
            self.logger.info(f"Evidence screenshot saved: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Screenshot error: {e}")
            raise
    
    async def shutdown(self):
        """Shutdown ARGUS agent"""
        self.logger.info("Shutting down ARGUS agent...")
        
        if self.selenium_driver:
            self.selenium_driver.quit()
        
        await super().shutdown()

# Agent registration function
def create_agent() -> ARGUSAgent:
    """Create and return ARGUS agent instance"""
    return ARGUSAgent()