from .check_root import (
    check_root_tag,
    check_namespace,
)
from .check_info import (
    check_info,
    check_info_revhistory,
    check_info_revhistory_revision,
    check_info_revhistory_revision_date,
    check_info_revhistory_revision_order,

)
from .check_meta import (
    check_meta_title,
    check_meta_description,
    check_meta_series,
    check_meta_techpartner,
    check_meta_platform,
    check_meta_architecture,
    check_meta_category,
    check_meta_task,
)

# Keep the order. The next item is dependent on the previous item.
__all__ = [
    "check_root_tag",
    "check_namespace",
    "check_info",
    #
    "check_info_revhistory",
    "check_info_revhistory_revision",
    "check_info_revhistory_revision_date",
    "check_info_revhistory_revision_order",
    #
    "check_meta_title",
    "check_meta_description",
    "check_meta_series",
    "check_meta_techpartner",
    "check_meta_platform",
    "check_meta_architecture",
    "check_meta_category",
    "check_meta_task",
]

