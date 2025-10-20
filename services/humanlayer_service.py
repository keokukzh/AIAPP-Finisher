"""
HumanLayer Service - Approval workflow integration for AI-powered code fixes

Provides human-in-the-loop patterns for safe AI code modifications.
Based on HumanLayer SDK for production-ready approval workflows.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class HumanLayerService:
    """
    Service for managing human approval workflows for AI actions.

    Integrates with HumanLayer SDK for:
    - Code fix approvals
    - Deployment confirmations
    - High-risk operation reviews
    """

    def __init__(self):
        """Initialize HumanLayer service with approval workflow"""
        self.approval_history = []
        self._initialized = False

        try:
            # Import HumanLayer SDK components
            from humanlayer import HumanLayer
            from humanlayer.core.approval import ApprovalMethod

            self.hl = HumanLayer(
                approval_method=ApprovalMethod.BACKEND,  # UI-based approval
                run_id_factory=lambda: f"fix_{datetime.now().timestamp()}",
            )
            self._initialized = True
            logger.info("✅ HumanLayer service initialized (approval workflows enabled)")

        except ImportError as e:
            logger.warning(f"⚠️ HumanLayer SDK not available: {e}")
            logger.info("💡 Install with: pip install humanlayer>=0.7.0")
            # Gracefully degrade - service works without HumanLayer
            self.hl = None

    async def request_approval(
        self, action_type: str, details: Dict[str, Any], channel: str = "code_fixes"
    ) -> Dict[str, Any]:
        """
        Request human approval for an AI action

        Args:
            action_type: Type of action (e.g., 'code_fix', 'deploy', 'delete')
            details: Action details (file, changes, impact, etc)
            channel: Communication channel for approval request

        Returns:
            Approval result with status and metadata
        """
        request_id = f"{action_type}_{datetime.now().timestamp()}"

        logger.info(f"📋 Approval requested: {action_type} (ID: {request_id})")

        approval_request = {
            "request_id": request_id,
            "action_type": action_type,
            "details": details,
            "channel": channel,
            "requested_at": datetime.now().isoformat(),
            "status": "pending",
        }

        # Store in history
        self.approval_history.append(approval_request)

        # If HumanLayer available, use it
        if self._initialized and self.hl:
            try:
                # HumanLayer handles the approval workflow
                # Returns when user approves/rejects
                logger.info("🔄 Waiting for HumanLayer approval...")
                # This would typically block until approval
                # For now, return pending status
                return {
                    "request_id": request_id,
                    "status": "pending",
                    "approval_url": f"/api/hl/approve/{request_id}",
                    "message": "Approval required - check approval UI",
                }
            except Exception as e:
                logger.error(f"❌ HumanLayer approval error: {e}")
                return {"request_id": request_id, "status": "error", "error": str(e)}
        else:
            # Fallback: auto-approve with warning
            logger.warning("⚠️ Auto-approving (HumanLayer not available)")
            approval_request["status"] = "auto_approved"
            return {
                "request_id": request_id,
                "status": "auto_approved",
                "message": "Auto-approved (HumanLayer SDK not installed)",
            }

    async def check_approval_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Check status of an approval request"""
        for request in self.approval_history:
            if request["request_id"] == request_id:
                return request
        return None

    async def approve(self, request_id: str, approver: str = "system") -> Dict[str, Any]:
        """Approve a pending request"""
        for request in self.approval_history:
            if request["request_id"] == request_id:
                request["status"] = "approved"
                request["approved_at"] = datetime.now().isoformat()
                request["approved_by"] = approver
                logger.info(f"✅ Request approved: {request_id} by {approver}")
                return request

        return {"error": "Request not found"}

    async def reject(self, request_id: str, reason: str = "") -> Dict[str, Any]:
        """Reject a pending request"""
        for request in self.approval_history:
            if request["request_id"] == request_id:
                request["status"] = "rejected"
                request["rejected_at"] = datetime.now().isoformat()
                request["rejection_reason"] = reason
                logger.info(f"❌ Request rejected: {request_id} - {reason}")
                return request

        return {"error": "Request not found"}

    def get_approval_history(self, limit: int = 50) -> list:
        """Get recent approval requests"""
        return self.approval_history[-limit:]

    def is_initialized(self) -> bool:
        """Check if HumanLayer SDK is available and initialized"""
        return self._initialized


# Global instance
_humanlayer_service = None


def get_humanlayer_service() -> HumanLayerService:
    """Get or create global HumanLayer service instance"""
    global _humanlayer_service
    if _humanlayer_service is None:
        _humanlayer_service = HumanLayerService()
    return _humanlayer_service
